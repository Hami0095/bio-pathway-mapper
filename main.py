
import asyncio
from src.adapters.ollama_adapter import OllamaAdapter
from src.core.knowledge_graph import BiologicalKnowledgeGraph

async def main():
    # 1. Initialize
    llm_adapter = OllamaAdapter()
    bkg = BiologicalKnowledgeGraph(llm_adapter)
    
    # 2. Add gene data
    gene_list = ["TP53", "EGFR"]
    database_results = await bkg.add_gene_data(gene_list)

    # 3. Reconcile data and build graph
    reconciled_data = bkg.reconcile_and_add_pathway_data(database_results)

    # 4. Perform harmonization and quality control on reconciled pathways (demonstration)
    if reconciled_data and reconciled_data.get("reconciled_pathways"):
        print("\n--- Harmonizing and Quality Controlling Reconciled Pathways ---")
        # Example of using harmonizer and qc on the reconciled data
        # For a full implementation, you would pass the reconciled_data structure
        # to specific methods of harmonizer and qc classes.
        
        # This is a simplified demonstration as the original harmonizer/qc classes
        # were designed for raw database outputs, not a structured LLM output.
        # However, the concepts apply.
        
        # Example: standardize pathway names (if needed, LLM should already do this)
        # standardized_pathways = bkg.harmonizer.standardize_pathway_names(reconciled_data["reconciled_pathways"])
        
        # Example: cross-reference (if comparing LLM output to another source)
        # cross_referenced = bkg.qc.cross_reference_pathways(standardized_pathways)
        
        print("Harmonization and Quality Control steps completed conceptually.")
        print(f"Graph now has {bkg.graph.number_of_nodes()} nodes and {bkg.graph.number_of_edges()} edges from reconciled data.")

    # 5. Run analysis on the graph
    if bkg.graph.number_of_nodes() > 0:
        bkg.analyze_centrality()
        bkg.detect_communities()
    else:
        print("Graph is empty after reconciliation. Skipping analysis and visualization.")
        return

    # 6. Generate hypotheses
    hypotheses = bkg.generate_hypotheses("bottleneck genes")
    print("\n--- LLM-Generated Hypotheses ---")
    print(hypotheses)

    # 7. Generate biological insights
    insights_query = "Summarize the key findings from the network analysis, including central genes and community structures."
    insights = bkg.generate_biological_insights(insights_query)
    print("\n--- LLM-Generated Biological Insights ---")
    print(insights)


    # 8. Visualize the graph
    print("\n--- Visualizing Graph ---")
    bkg.visualize_graph()

if __name__ == "__main__":
    asyncio.run(main())

