from typing import List, Dict, Any
from ..core.database_connector import DatabaseConnector
from ..legacy_connectors.database_connectors import LegacyUniProtConnector, APIClient

class UniProtConnector(DatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__("UniProt", api_client)
        self.legacy_uniprot_connector = LegacyUniProtConnector(api_client)
        
    async def fetch_genes(self, gene_list: List[str]) -> Dict:
        if not gene_list:
            return {}
        # UniProt's fetch_genes will return detailed info for each gene in the list
        all_uniprot_info = {}
        for gene_id in gene_list:
            info = await self.legacy_uniprot_connector.get_uniprot_info(gene_id)
            if info:
                all_uniprot_info[gene_id] = info
        return {"source": self.name, "genes": gene_list, "info": all_uniprot_info}

    def parse_response(self, response: Any) -> Dict:
        return response