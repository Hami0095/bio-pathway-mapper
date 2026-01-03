import asyncio
import aiohttp
import pickle
import os
from pyprojroot import here
from lxml import etree
import reactome2py
from reactome2py.analysis import identifier
import functools # Import functools
import json # Ensure json is imported for json.loads in _get


class APIClient:
    """Handles low-level HTTP requests, caching, and rate limiting."""
    def __init__(self, cache_dir=here("cache"), rate_limit: float = 0.1):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.session = None
        self.rate_limit = rate_limit
        self._last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def _get(self, url, params=None, headers=None, response_format="json"):
        if isinstance(params, str):
            url = f"{url}?{params}"
            params = None

        cache_key = str(url) + str(params) + str(headers) + response_format
        cache_file = os.path.join(self.cache_dir, f"{hash(cache_key)}.pkl")

        if os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                return pickle.load(f)

        # Apply rate limiting
        current_time = asyncio.get_event_loop().time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.rate_limit:
            await asyncio.sleep(self.rate_limit - time_since_last_request)
        self._last_request_time = asyncio.get_event_loop().time()

        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                response.raise_for_status() # Raise an exception for HTTP errors
                if response_format == "json":
                    try:
                        data = await response.json()
                    except aiohttp.ContentTypeError:
                        text_content = await response.text()
                        data = json.loads(text_content)
                elif response_format == "xml":
                    data = etree.fromstring(await response.read())
                elif response_format == "text":
                    data = await response.text()
                else:
                    data = await response.read() # raw bytes

                with open(cache_file, "wb") as f:
                    pickle.dump(data, f)

                return data
        except aiohttp.ClientError as e:
            print(f"Error fetching {url}: {e}")
            return None


class LegacyDatabaseConnector:
    """Base class for legacy database-specific API logic using an APIClient."""
    def __init__(self, api_client: APIClient):
        self.api_client = api_client


class LegacyKEGGConnector(LegacyDatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client)
        self.base_url = "http://rest.kegg.jp"

    async def get_kegg_pathways(self, uniprot_id: str):
        # Convert UniProt ID to KEGG Gene ID
        conv_url = f"{self.base_url}/conv/genes/uniprot:{uniprot_id}"
        conv_data = await self.api_client._get(conv_url, response_format="text")
        if not conv_data:
            return []

        try:
            kegg_gene_id = conv_data.strip().split('\t')[1]
        except IndexError:
            return []

        # Get all human KEGG pathways and create an ID to name mapping
        list_pathway_url = f"{self.base_url}/list/pathway/hsa"
        list_pathway_data = await self.api_client._get(list_pathway_url, response_format="text")
        kegg_pathway_name_map = {}
        if list_pathway_data:
            for line in list_pathway_data.strip().split('\n'):
                parts = line.split('\t')
                if len(parts) > 1:
                    path_id = parts[0].replace('path:', '')
                    path_name = parts[1]
                    kegg_pathway_name_map[path_id] = path_name

        # Find pathways linked to the KEGG Gene ID
        link_url = f"{self.base_url}/link/pathway/{kegg_gene_id}"
        link_data = await self.api_client._get(link_url, response_format="text")
        if not link_data:
            return []

        pathway_ids = [line.split('\t')[1].replace('path:', '') for line in link_data.strip().split('\n')]

        # Get pathway names from the map
        pathways = []
        for pathway_id in pathway_ids:
            if pathway_id in kegg_pathway_name_map:
                pathways.append({"id": pathway_id, "name": kegg_pathway_name_map[pathway_id]})
            else:
                print(f"Warning: KEGG pathway ID {pathway_id} not found in name map.")

        return pathways


class LegacyReactomeConnector(LegacyDatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client)

    async def get_reactome_pathways(self, uniprot_id: str):
        loop = asyncio.get_event_loop()
        analysis_result = await loop.run_in_executor(
            None,
            lambda: identifier( # Wrap in lambda to pass keyword arguments
                uniprot_id,
                species="Homo sapiens",
                resource="UNIPROT"
            )
        )

        pathways = []
        if analysis_result and "pathways" in analysis_result:
            for pathway_hit in analysis_result["pathways"]:
                if "stId" in pathway_hit and "name" in pathway_hit:
                    pathways.append({"id": pathway_hit["stId"], "name": pathway_hit["name"]})
                elif "stId" in pathway_hit and "displayName" in pathway_hit: # Fallback to displayName if 'name' is not present
                     pathways.append({"id": pathway_hit["stId"], "name": pathway_hit["displayName"]})
        return pathways


class LegacyStringConnector(LegacyDatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client)
        self.base_url = "https://string-db.org/api/json/network"

    async def get_string_interactions(self, gene_list: list):
        url = self.base_url
        params = f"identifiers={'%0d'.join(gene_list)}&species=9606"
        return await self.api_client._get(url, params=params)


class LegacyUniProtConnector(LegacyDatabaseConnector):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client)
        self.base_url = "https://rest.uniprot.org/uniprotkb/search"

    async def get_uniprot_info(self, gene_id: str):
        url = self.base_url
        params = {"query": f"gene:{gene_id} AND organism_id:9606", "format": "json"}
        return await self.api_client._get(url, params=params)