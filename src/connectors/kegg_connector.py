from typing import List, Dict, Any
from ..core.database_connector import DatabaseConnector
from ..legacy_connectors.database_connectors import LegacyKEGGConnector, APIClient

class KEGGConnector(DatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__("KEGG", api_client)
        self.legacy_kegg_connector = LegacyKEGGConnector(api_client)
        
    async def fetch_genes(self, gene_list: List[str]) -> Dict:
        # Assuming gene_list contains UniProt IDs for now
        # In a real scenario, you'd map gene_list to UniProt IDs if necessary
        # For simplicity, we'll fetch pathways for the first gene in the list
        if not gene_list:
            return {}
        uniprot_id_for_query = gene_list[0] # This is a simplification

        pathways = await self.legacy_kegg_connector.get_kegg_pathways(uniprot_id_for_query)
        return {"source": self.name, "genes": gene_list, "pathways": pathways}

    def parse_response(self, response: Any) -> Dict:
        # The fetch_genes method already returns a structured dict
        return response