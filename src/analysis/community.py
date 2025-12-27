
import networkx as nx
from networkx.algorithms import community

def detect_louvain_communities(graph: nx.MultiDiGraph) -> list:
    """
    Detects communities in the graph using the Louvain method.
    Note: The Louvain algorithm is for undirected graphs. We'll work with an
    undirected view of the graph.
    """
    if graph.is_directed():
        undirected_graph = graph.to_undirected()
    else:
        undirected_graph = graph

    # The Louvain method in networkx returns a list of sets of nodes.
    communities = community.louvain_communities(undirected_graph)
    return communities
