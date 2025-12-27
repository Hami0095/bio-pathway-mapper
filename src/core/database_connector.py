
from typing import List, Dict, Any
import asyncio # Add asyncio import

class DatabaseConnector:
    """Base class for all database connections"""
    def __init__(self, name: str, api_client: Any): # Add api_client
        self.name = name
        self.api_client = api_client # Store api_client
        
    async def fetch_genes(self, gene_list: List[str]) -> Dict:
        """Fetch gene data - implement per database"""
        raise NotImplementedError
        
    def parse_response(self, response: Any) -> Dict:
        """Parse database-specific response"""
        raise NotImplementedError
