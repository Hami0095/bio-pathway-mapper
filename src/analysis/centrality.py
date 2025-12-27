
import networkx as nx

def calculate_degree_centrality(graph: nx.MultiDiGraph) -> dict:
    """Calculates degree centrality for each node in the graph."""
    return nx.degree_centrality(graph)

def calculate_betweenness_centrality(graph: nx.MultiDiGraph) -> dict:
    """Calculates betweenness centrality for each node in the graph."""
    return nx.betweenness_centrality(graph)

def calculate_closeness_centrality(graph: nx.MultiDiGraph) -> dict:
    """Calculates closeness centrality for each node in the graph."""
    return nx.closeness_centrality(graph)

def calculate_eigenvector_centrality(graph: nx.MultiDiGraph) -> dict:
    """Calculates eigenvector centrality for each node in the graph."""
    # Eigenvector centrality is not implemented for MultiDiGraph.
    # We create a simple DiGraph for this calculation.
    if isinstance(graph, (nx.MultiDiGraph, nx.MultiGraph)):
        # Create a DiGraph, keeping only one edge for any parallel edges
        simple_graph = nx.Graph() # Use Graph for undirected eigenvector centrality
        for u, v, k in graph.edges(keys=True):
            if not simple_graph.has_edge(u, v):
                simple_graph.add_edge(u, v)
        graph_to_analyze = simple_graph
    else:
        graph_to_analyze = graph

    try:
        # It's common to calculate eigenvector on the undirected version of the graph
        # to capture overall influence regardless of direction.
        return nx.eigenvector_centrality(graph_to_analyze)
    except nx.PowerIterationFailedConvergence:
        print("Warning: Eigenvector centrality did not converge.")
        return {}
