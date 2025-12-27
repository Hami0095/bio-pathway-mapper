
class Config:
    OLLAMA_BASE_URL = "http://localhost:11434"
    DEFAULT_MODEL = "llama2"
    CACHE_DIR = "./cache"
    RATE_LIMITS = {
        'kegg': 1.0,  # seconds between requests
        'uniprot': 0.5,
        'reactome': 1.0
    }
    MAX_JSON_RETRIES = 3 # Max retries for LLM to produce valid JSON
