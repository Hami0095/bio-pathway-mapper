# Biological Pathway Mapping and Analysis

This project provides a Streamlit web application to analyze biological pathways from a list of genes. It uses a combination of public biological databases and a local Large Language Model (LLM) via Ollama to build, reconcile, and visualize a knowledge graph of genes and their associated pathways.

## Features

-   **Easy Gene Input**: Paste a list of genes separated by newlines or commas.
-   **1-Click Analysis**: Automatically fetches data, builds a knowledge graph, and runs analysis.
-   **LLM-Powered Insights**: Generates hypotheses and biological insights from the network structure.
-   **Interactive Visualization**: Displays the resulting gene-pathway graph.

## How It Works

1.  **Data Fetching**: Gathers pathway and interaction data from KEGG, Reactome, UniProt, and STRING-DB.
2.  **LLM Reconciliation**: Uses a local LLM (via Ollama) to clean, merge, and reconcile the data from the different sources into a coherent set of pathways.
3.  **Graph Analysis**: Builds a network graph and analyzes it to find central nodes and communities.
4.  **Insight Generation**: Feeds the analysis results back into the LLM to generate plain-language hypotheses and summaries.
5.  **Streamlit UI**: Provides a simple web interface for users to input genes and see the results.

---

## Getting Started: Local Setup

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

1.  **Git**: To clone the repository.
2.  **Python 3.9+**: To run the application.
3.  **Ollama**: To run the local Large Language Model.
    -   [Download and install Ollama](https://ollama.ai/) for your operating system (macOS, Linux, or Windows).
    -   After installing, you must pull at least one model. Open your terminal and run:
        ```bash
        ollama pull gemma3:1b
        ```
    -   **Default Model Note**: `gemma3:1b` is a relatively small and manageable model, suitable for most modern laptops.
    -   **Optional Powerful Model**: For more detailed and nuanced insights, you can also pull a larger model:
        ```bash
        ollama pull gpt:oss120b-cloud
        ```
        `gpt:oss120b-cloud` is a very large model and requires significant computational resources (e.g., a powerful CPU and ample RAM, or a GPU) to run effectively. If you choose to use this model, you will need to update the `src/adapters/ollama_adapter.py` file to specify `gpt:oss120b-cloud` as the model name.

### Installation and Setup

Follow these steps to set up the project environment.

**1. Clone the Repository**

Open your terminal or command prompt and clone the repository to your local machine:

```bash
git clone https://github.com/Hami0095/bio-pathway-mapper.git
cd bio-pathway-mapper/biological_kg
```

**2. Create and Activate a Python Virtual Environment**

It's highly recommended to use a virtual environment to manage project dependencies.

*   **On macOS/Linux:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
*   **On Windows:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

**3. Install Dependencies**

With your virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Once the setup is complete, you can run the Streamlit application.

**1. Ensure Ollama is Serving the Model**

Make sure the Ollama application is running on your machine. You can check this by looking for the Ollama icon in your system's menu bar or taskbar.

**2. Launch the Streamlit App**

In your terminal (with the virtual environment still activated), run the following command:

```bash
streamlit run streamlit_app.py
```

This will open the application in a new tab in your default web browser. You can now start using the tool!

## Credits
- **Abdur Rehman** - [LinkedIn](https://www.linkedin.com/in/your-linkedin-profile)

## Future Work

We plan to create an "Automated Setup Agent" that will download and complete the setup of installing the model on users' computers and will launch the Streamlit app on their browsers along with the Ollama server. You can track the progress of this feature in [Issue #1](https://github.com/Hami0095/bio-pathway-mapper/issues/1) (this is a placeholder link).
