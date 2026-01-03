import streamlit as st
import asyncio
import re
from src.adapters.ollama_adapter import OllamaAdapter
from src.core.knowledge_graph import BiologicalKnowledgeGraph
from main import main as main_analysis

st.title("Pathway Analysis")

gene_input = st.text_area("Enter gene names (one per line, or separated by commas)")

if st.button("Run Pathway Analysis"):
    st.write("Running analysis...")
    
    # Split by commas or newlines and remove any whitespace
    gene_list = [gene.strip() for gene in re.split(r'[,\n]', gene_input) if gene.strip()]

    if gene_list:
        hypotheses, insights, graph_viz = asyncio.run(main_analysis(gene_list))

        st.subheader("Hypotheses")
        st.write(hypotheses)

        st.subheader("Biological Insights")
        st.write(insights)

        st.subheader("Graph Visualization")
        if graph_viz:
            st.pyplot(graph_viz)
        else:
            st.write("Could not generate graph visualization.")
    else:
        st.write("Please enter at least one gene.")

    st.write("Analysis complete!")
