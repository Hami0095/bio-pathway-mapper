from typing import List, Dict
import networkx as nx
import asyncio
import json
from ..adapters.llm_adapter import LLMAdapter
from ..analysis import centrality, community
from ..utils import visualization
from ..connectors.kegg_connector import KEGGConnector
from ..connectors.reactome_connector import ReactomeConnector
from ..connectors.uniprot_connector import UniProtConnector
from ..connectors.string_connector import StringConnector # New import for STRING
from ..legacy_connectors.database_connectors import APIClient # Import APIClient
from ..legacy_connectors.data_harmonization import DataHarmonizer # Import DataHarmonizer
from ..legacy_connectors.quality_control import QualityControl # Import QualityControl


class BiologicalKnowledgeGraph:
    def __init__(self, llm_adapter: LLMAdapter):
        self.graph = nx.MultiDiGraph()
        self.llm = llm_adapter
        self.centrality_scores = {}
        self.communities = []
        self.harmonizer = DataHarmonizer() # Instantiate DataHarmonizer
        self.qc = QualityControl() # Instantiate QualityControl
        
        # Initialize APIClient once and pass to all connectors
        self.api_client = APIClient() 
        self.databases = {
            'kegg': KEGGConnector(self.api_client),
            'reactome': ReactomeConnector(self.api_client),
            'uniprot': UniProtConnector(self.api_client),
            'string': StringConnector(self.api_client) # Add STRING connector
        }

    async def __aenter__(self):
        # Ensure APIClient's session is managed
        await self.api_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.api_client.__aexit__(exc_type, exc, tb)

    async def add_gene_data(self, gene_list: List[str]):
        """
        Fetches data from multiple databases in parallel for a list of genes.
        """
        # Ensure APIClient's session is active for this context
        async with self.api_client:
            tasks = [db.fetch_genes(gene_list) for db in self.databases.values()]
            database_raw_results = await asyncio.gather(*tasks)
            
            processed_results = {}
            for result in database_raw_results:
                if result and "source" in result:
                    processed_results[result["source"].lower()] = result

            return processed_results

    def reconcile_and_add_pathway_data(self, database_results: Dict):
        """
        Uses an LLM to reconcile pathway data from multiple sources and adds it to the graph.
        """
        prompt = f"""
        You are a JSON API that processes biological pathway data. 

        INPUT DATA:
        {json.dumps(database_results, indent=2)}

        IMPORTANT: Return ONLY valid JSON. No explanations, no code, no markdown.

        OUTPUT FORMAT:
        {{
        "reconciled_pathways": [
            {{
            "pathway_id": "string",
            "pathway_name": "string", 
            "genes": ["array", "of", "genes"],
            "source_databases": ["array", "of", "db", "names"],
            "confidence": float
            }}
        ],
        "conflicts": [
            {{
            "pathway_id": "string",
            "issue": "string",
            "databases": ["array"],
            "resolution": "string"
            }}
        ],
        "confidence_scores": {{"pathway_id": float}},
        "recommendations": ["array", "of", "strings"]
        }}

        TASK: Process the input data and return JSON only.
        """
        reconciled_data = self.llm.generate_text(prompt, json_output=True)
        
        if isinstance(reconciled_data, dict) and not reconciled_data.get("error"):
            # Now, add the reconciled data to the graph
            for pathway in reconciled_data.get("reconciled_pathways", []):
                pathway_id = pathway.get("pathway_id")
                pathway_name = pathway.get("pathway_name", "Unknown Pathway")
                self.graph.add_node(pathway_id, name=pathway_name, type="pathway")
                for gene in pathway.get("genes", []):
                    self.graph.add_node(gene, type="gene")
                    self.graph.add_edge(gene, pathway_id, relation="participates_in")

            return reconciled_data

        else:
            return None
        
    def generate_biological_insights(self, query: str) -> str:
        """
        Uses the LLM to analyze the network and generate insights based on a query.
        """
        if not self.centrality_scores or not self.communities:
            return "Analysis has not been run. Please run analysis first."

        # Create a summary of the analysis results to use in the prompt
        prompt_context = f"Here is a summary of a biological network analysis:\n"
        prompt_context += f"- The network has {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.\n"
        
        prompt_context += "\n--- Top 5 Most Central Nodes (by Degree) ---\n"
        for node, score in self.get_top_n_central_nodes('degree', n=5):
            prompt_context += f"- {node}: {score:.4f}\n"

        prompt_context += "\n--- Detected Communities ---\n"
        for i, community_nodes in enumerate(self.communities):
            prompt_context += f"- Community {i+1}: {', '.join(map(str, community_nodes))}\n"

        # Combine with the user's query
        full_prompt = f"{prompt_context}\nBased on this analysis, please answer the following question: {query}"

        # Call the LLM to generate insights
        insights = self.llm.generate_text(full_prompt)
        return insights

    def generate_hypotheses(self, topic: str, n_bottlenecks: int = 3) -> str:
        """
        Generates hypotheses about a given topic, using network analysis results.
        Example topic: "bottleneck genes"
        """
        if not self.centrality_scores:
            return "Analysis has not been run. Please run analysis first."

        prompt_context = ""
        if topic == "bottleneck genes":
            prompt_context = "The following genes have been identified as potential bottlenecks in the network due to their high betweenness centrality:\n"
            bottlenecks = self.get_top_n_central_nodes('betweenness', n=n_bottlenecks)
            for node, score in bottlenecks:
                prompt_context += f"- {node} (Betweenness Centrality: {score:.4f})\n"
        
        full_prompt = f"""
        {prompt_context}
        Based on this information, please generate 3-5 testable hypotheses about the biological role of these potential bottleneck genes in the context of the network.
        Provide a brief explanation for each hypothesis.
        """

        hypotheses = self.llm.generate_text(full_prompt)
        return hypotheses

    def analyze_centrality(self, use_cache: bool = True) -> None:
        """
        Performs a full centrality analysis on the graph and stores the results.
        Uses a simple in-memory cache to avoid re-calculation.
        """
        if use_cache and self.centrality_scores:
            return

        self.centrality_scores['degree'] = centrality.calculate_degree_centrality(self.graph)
        self.centrality_scores['betweenness'] = centrality.calculate_betweenness_centrality(self.graph)
        self.centrality_scores['closeness'] = centrality.calculate_closeness_centrality(self.graph)
        self.centrality_scores['eigenvector'] = centrality.calculate_eigenvector_centrality(self.graph)

    def get_top_n_central_nodes(self, centrality_type: str, n: int = 10) -> List[tuple]:
        """
        Gets the top N nodes for a given centrality type.

        :param centrality_type: One of 'degree', 'betweenness', 'closeness', 'eigenvector'.
        :param n: The number of top nodes to return.
        :return: A list of (node, score) tuples.
        """
        if centrality_type not in self.centrality_scores:
            return []
        
        scores = self.centrality_scores[centrality_type]
        sorted_nodes = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return sorted_nodes[:n]

    def detect_communities(self) -> None:
        """
        Detects communities in the graph using the Louvain method and stores the result.
        """
        self.communities = community.detect_louvain_communities(self.graph)

    def visualize_graph(self):
        """
        Generates and displays a visualization of the graph.
        """
        if not self.graph:
            return
            
        centrality_for_sizing = self.centrality_scores.get('degree', {})
        return visualization.draw_graph(self.graph, self.communities, centrality_for_sizing)