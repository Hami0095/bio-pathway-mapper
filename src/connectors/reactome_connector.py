from typing import List, Dict, Any
from ..core.database_connector import DatabaseConnector
from ..legacy_connectors.database_connectors import LegacyReactomeConnector, APIClient

class ReactomeConnector(DatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__("Reactome", api_client)
        self.legacy_reactome_connector = LegacyReactomeConnector(api_client)
        
    async def fetch_genes(self, gene_list: List[str]) -> Dict:
        if not gene_list:
            return {}
        uniprot_id_for_query = gene_list[0] # This is a simplification
        pathways = await self.legacy_reactome_connector.get_reactome_pathways(uniprot_id_for_query)
        return {"source": self.name, "genes": gene_list, "pathways": pathways}

    def parse_response(self, response: Any) -> Dict:
        return response