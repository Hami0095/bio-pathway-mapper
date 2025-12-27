
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
        
        # STRING API often takes a single UniProt ID or a list of identifiers
        # For simplicity, we'll fetch interactions for the first gene in the list
        uniprot_id_for_query = gene_list[0] # This is a simplification
        interactions = await self.legacy_string_connector.get_string_interactions(uniprot_id_for_query)
        return {"source": self.name, "genes": gene_list, "interactions": interactions}

    def parse_response(self, response: Any) -> Dict:
        return response
