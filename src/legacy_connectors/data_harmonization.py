
import pandas as pd
import mygene

class DataHarmonizer:
    def __init__(self):
        self.mg = mygene.MyGeneInfo()

    def map_gene_ids(self, gene_ids, scopes="entrezgene,ensembl.gene", species="human"):
        if not isinstance(gene_ids, list):
            gene_ids = [gene_ids]
        results = self.mg.querymany(gene_ids, scopes=scopes, species=species, as_dataframe=True)
        return results

    def standardize_pathway_names(self, pathways):
        # A simple example of a synonym map
        synonym_map = {
            "cell cycle": "Cell Cycle",
            "metabolism": "Metabolism",
            "dna replication": "DNA Replication",
        }

        standardized_pathways = []
        for pathway in pathways:
            name = pathway["name"].lower()
            standardized_name = synonym_map.get(name, pathway["name"])
            standardized_pathways.append({"id": pathway["id"], "name": standardized_name, "source": pathway.get("source")})
        return standardized_pathways

    def create_unified_ontology(self, pathways):
        # A simple example of an ontology mapping
        ontology_map = {
            "Metabolism": ["metabolism", "metabolic"],
            "Signaling": ["signaling", "signal"],
            "Cell Cycle": ["cell cycle", "cycle"],
            "DNA Replication": ["dna replication", "replication"],
        }

        unified_ontology = {category: [] for category in ontology_map}

        for pathway in pathways:
            name = pathway["name"].lower()
            for category, keywords in ontology_map.items():
                if any(keyword in name for keyword in keywords):
                    unified_ontology[category].append(pathway)

        return unified_ontology
