<!-- # Biological Knowledge Graph System

## Overview
This project implements a modular Biological Knowledge Graph (BKG) system designed to integrate biological data from multiple sources, analyze complex networks, and generate biological insights and hypotheses using Large Language Models (LLMs).

## Features
- **LLM Adapter Layer**: Abstract interface for different LLM backends (currently supporting Ollama).
- **Multi-Database Integration**: Connectors for KEGG, Reactome, UniProt, and STRING databases, leveraging pre-existing robust API integration logic.
- **Data Harmonization**: Tools for mapping gene identifiers, standardizing pathway names, and creating unified ontologies.
- **Network Analysis Engine**:
    - **Centrality Analysis**: Calculates various centrality measures (degree, betweenness, closeness, eigenvector) to identify key nodes (e.g., bottleneck genes) in the network.
    - **Community Detection**: Utilizes algorithms like Louvain method to find natural groupings or modules within the biological network.
- **Biological Insight Generator**: Uses LLMs to interpret network analysis results, reconcile conflicting data, assign confidence scores, and generate human-readable explanations.
- **Hypothesis Generation Engine**: Leverages LLMs to formulate testable hypotheses based on network patterns and identified critical nodes.
- **Visualization Support**: Generates graphical representations of the knowledge graph, highlighting central nodes and communities.
- **Caching**: Implements a caching layer to store API responses and analysis results, improving performance and reducing redundant calls.

## Why is this Model Revolutionizing?
This BKG system offers a revolutionary approach to biological data analysis by:
- **Intelligent Data Integration**: Moving beyond simple data aggregation, it uses LLMs to intelligently reconcile conflicting information from diverse biological databases, assigning confidence scores and suggesting resolutions.
- **Automated Hypothesis Generation**: It automates the generation of testable biological hypotheses, enabling researchers to quickly identify promising avenues for further investigation. This accelerates the discovery process by focusing experimental efforts.
- **Actionable Insights**: By combining advanced network analysis with LLM interpretation, the system provides not just data, but actionable biological insights in natural language, making complex network patterns understandable and interpretable.
- **Modularity and Extensibility**: Its modular architecture (LLM adapter, database connectors) allows for easy integration of new databases, LLM models, and analysis techniques, ensuring future-proofing and adaptability.
- **Bottleneck Identification**: Pinpointing bottleneck genes and pathways allows researchers to identify critical control points in biological systems, which are prime targets for therapeutic intervention or fundamental biological study.

## Setup

### Prerequisites
- Python 3.8+
- **Ollama**: For LLM integration, you need to have the Ollama server running locally. Download and install it from [ollama.ai](https://ollama.ai/). Ensure you have a model pulled (e.g., `minimax-m2`) and running.
  - By default, the system tries to connect to Ollama at `http://localhost:11434`.
- **Python Dependencies**:
  `requests`
  `networkx`
  `numpy`
  `aiohttp`
  `h5py` (if using file-based HDF5 caching, not currently implemented but specified in original prompt)
  `pyprojroot`
  `mygene`
  `lxml`
  `reactome2py`
  `matplotlib`
  `scipy` # Required for some networkx functions
  `pandas` # Used in legacy harmonizer
  `beautifulsoup4` # Dependency of bioservices
  `bioservices` # Dependency in initial prompt, used by some legacy code
  `tqdm` # Dependency of bioservices
  `wrapt` # Dependency of bioservices
  `xmltodict` # Dependency of bioservices

### Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd biological_kg
    ```
    *(Assuming you are already in the `biological_kg` directory)*

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source ./.venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing some dependencies, install them manually)*

## How to Run and Test

1.  **Ensure Ollama is Running**:
    Start your Ollama server and pull the `llama2` model:
    ```bash
    ollama run llama2
    ```
    Leave this running in a separate terminal or as a background service.

2.  **Execute the Main Application**:
    Navigate to the `biological_kg` directory and run the `main.py` script:
    ```bash
    python main.py
    ```

## Expected Output

The script will:
- Fetch placeholder data from simulated database connectors.
- Print raw database results.
- Call the Ollama LLM (or use mock data if Ollama is not running) to reconcile pathway data, identifying conflicts, assigning confidence scores, and providing recommendations.
- Build a knowledge graph based on the reconciled data.
- Perform centrality analysis and community detection.
- Call the Ollama LLM (or use mock data) to generate biological hypotheses about bottleneck genes.
- Call the Ollama LLM (or use mock data) to generate biological insights based on network analysis.
- Attempt to visualize the graph (a warning will be printed if no GUI environment is detected).

## Future Enhancements
- Implement a persistent caching layer (e.g., Redis, HDF5).
- Develop comprehensive unit tests for all components.
- Create an interactive web interface (e.g., using Flask/FastAPI and a frontend framework).
- Implement more sophisticated data harmonization and conflict resolution algorithms.
- Expand database connectors to full API implementations.
- Add support for more LLM providers. -->

