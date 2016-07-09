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

    # def get_waypoints_for_plotting(self):
    #     """ converts road graph to x and y arrays, a convenience function for plotting for matplotlib """
    #     x = []
    #     y = []
    #     for node, nodes in self.items():
    #         x.append([node[0]] + [n[0] for n in nodes])
    #         y.append([node[1]] + [n[1] for n in nodes])
    #     return x, y

    def traverse(self):
        """
        Traverses the road graph and returns pairs of neighboring waypoints.

        :rtype iterator
        """
        for node, following_nodes in self.items():
            for fn in following_nodes:
                yield (node, fn)

    def traverse_paths(self, node=None, length=1):
        """
        Traverses the graph for paths of the required length.

        :param node: starting node; if None, then all graph nodes are analyzed once
        :param length: Length of each path segment.
        :rtype iterator
        """
        # print('Node: ', node)
        if node is None:
            for node in self:
                for path in self.traverse_paths(node, length):
                    yield path

        elif node not in self:
            return  # node has no children

        else:
            if length == 1:
                for child in self[node]:
                    yield [node, child]

            else:
                for child in self[node]:
                    for path in self.traverse_paths(child, length-1):
                        yield [node] + path
