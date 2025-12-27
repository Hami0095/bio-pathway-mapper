
import pandas as pd

class QualityControl:
    def __init__(self):
        pass

    def cross_reference_pathways(self, pathways):
        cross_referenced = {}
        for pathway in pathways:
            name = pathway["name"]
            source = pathway["source"]
            if name not in cross_referenced:
                cross_referenced[name] = {"sources": []}
            cross_referenced[name]["sources"].append(source)
        return cross_referenced

    def calculate_confidence_scores(self, cross_referenced_pathways):
        for name, data in cross_referenced_pathways.items():
            data["confidence_score"] = len(data["sources"])
        return cross_referenced_pathways

    def flag_conflicts(self, scored_pathways):
        for name, data in scored_pathways.items():
            if data["confidence_score"] == 1:
                data["conflict"] = "Only found in one database"
        return scored_pathways
