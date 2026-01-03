
import asyncio
from src.adapters.ollama_adapter import OllamaAdapter
from src.core.knowledge_graph import BiologicalKnowledgeGraph

async def main(gene_list):
    # 1. Initialize
    llm_adapter = OllamaAdapter()
    bkg = BiologicalKnowledgeGraph(llm_adapter)
    
    # 2. Add gene data
    database_results = await bkg.add_gene_data(gene_list)

    # 3. Reconcile data and build graph
    reconciled_data = bkg.reconcile_and_add_pathway_data(database_results)

    # 4. Perform harmonization and quality control on reconciled pathways (demonstration)
    if reconciled_data and reconciled_data.get("reconciled_pathways"):
        pass

    # 5. Run analysis on the graph
    if bkg.graph.number_of_nodes() > 0:
        bkg.analyze_centrality()
        bkg.detect_communities()
    else:
        return None, None, None

    # 6. Generate hypotheses
    hypotheses = bkg.generate_hypotheses("bottleneck genes")

    # 7. Generate biological insights
    insights_query = "Summarize the key findings from the network analysis, including central genes and community structures."
    insights = bkg.generate_biological_insights(insights_query)


    # 8. Visualize the graph
    fig = bkg.visualize_graph()

    return hypotheses, insights, fig

if __name__ == "__main__":
    asyncio.run(main(["TP53", "EGFR"]))

