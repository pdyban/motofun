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

    def get_waypoints_for_plotting(self):
        """ converts road graph to x and y arrays, a convenience function for plotting for matplotlib """
        x = []
        y = []
        for node, nodes in self.items():
            x.append([node[0]] + [n[0] for n in nodes])
            y.append([node[1]] + [n[1] for n in nodes])
        return x, y
