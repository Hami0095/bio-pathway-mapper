
from typing import List, Dict, Any
from ..core.database_connector import DatabaseConnector
from ..legacy_connectors.database_connectors import LegacyStringConnector, APIClient

class StringConnector(DatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__("STRING", api_client)
        self.legacy_string_connector = LegacyStringConnector(api_client)
        
    async def fetch_genes(self, gene_list: List[str]) -> Dict:
        if not gene_list:
            return {}
        
        interactions = await self.legacy_string_connector.get_string_interactions(gene_list)
        return {"source": self.name, "genes": gene_list, "interactions": interactions}

    def parse_response(self, response: Any) -> Dict:
        return response
