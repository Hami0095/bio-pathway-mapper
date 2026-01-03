
import networkx as nx
import matplotlib.pyplot as plt
import random
import os

def draw_graph(graph: nx.MultiDiGraph, communities: list = None, centrality: dict = None):
    """
    Draws the graph using matplotlib, with options to color by community and size by centrality.
    """
    fig = plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph, seed=42)

    # Node colors based on communities
    node_colors = "#A0CBE2" # Default color
    if communities:
        # Create a color map for communities
        community_colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(len(communities))]
        color_map = {}
        for i, community_nodes in enumerate(communities):
            for node in community_nodes:
                color_map[node] = community_colors[i]
        
        node_colors = [color_map.get(node, "#A0CBE2") for node in graph.nodes()]

    # Node sizes based on centrality
    node_sizes = 300
    if centrality:
        # Normalize centrality values for better visualization
        max_centrality = max(centrality.values()) if centrality else 1
        node_sizes = [(centrality.get(node, 0) / max_centrality) * 5000 + 300 for node in graph.nodes()]


    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=8)

    plt.title("Biological Knowledge Graph")
    return fig
