import networkx as nx
import mplleaflet


def draw_road_graph(graph, draw_edges=True, draw_nodes=True):
    """
    Plots nodes and edges of a road graph, overlays the graph over the world map.

    :param graph: the road graph that shall be plotted
    :type graph: RoadGraphX
    :param draw_edges: should plot edges
    :param draw_nodes: should plot nodes
    :return:
    """
    pos = {}
    for node in graph.graph.nodes():
        pos[node] = [float(i) for i in node]

    colors = []
    for start, finish, edge_data in graph.graph.edges(data=True):
        colors.append(edge_data['fun_factor'])
    if draw_nodes:
        nx.draw_networkx_nodes(graph.graph, pos=pos, node_size=10)
    if draw_edges:
        nx.draw_networkx_edges(graph.graph, pos=pos, edge_color=colors, width=5)

    return mplleaflet.display()
