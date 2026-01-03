import streamlit as st
import asyncio
import re
import requests
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

st.divider()

st.header("Debug Tools")
st.subheader("Ollama Connection Test")

if st.button("Test Ollama Connection"):
    with st.spinner("Attempting to connect to Ollama..."):
        try:
            # Attempt to connect to the Ollama /api/tags endpoint
            response = requests.get("http://127.0.0.1:11434/api/tags")
            
            # Raise an exception if the status code is not 2xx
            response.raise_for_status()
            
            st.success("Successfully connected to Ollama!")
            st.write("Models available:")
            st.json(response.json())
            
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to Ollama.")
            st.write("Error Details:")
            st.code(str(e))
            st.warning(
                "Please ensure the Ollama server is running and accessible. "
                "Check for firewalls or CORS issues. The 'OLLAMA_ORIGINS' environment variable "
                "may need to be configured to allow requests from the Streamlit application's origin."
            )
