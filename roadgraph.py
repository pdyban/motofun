from collections import defaultdict


class RoadGraph(defaultdict):
    """
    Graph implementation for easy access
    """
    def __init__(self):
        defaultdict.__init__(self, dict)

    def append_way(self, nodes):
        """
        Stores list of waypoints.

        :param nodes: list of waypoints
        :return:
        """
        for prev_node, cur_node in zip(nodes[:-1], nodes[1:]):
            self[prev_node][cur_node] = 0.0
