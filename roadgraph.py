from collections import defaultdict
from copy import deepcopy


class RoadGraph(defaultdict):
    """
    Graph implementation for easy access.

    :param memo: parameter for deepcopy operator.
    """
    def __init__(self, memo=None):
        super().__init__(dict)

    def edges(self):
        """
        Returns a list of all edges in the graph.

        :rtype: list
        """
        return [s for s in self.traverse_paths()]

    def append_way(self, nodes):
        """
        Stores list of waypoints.

        :param nodes: list of waypoints
        :return:
        """
        for prev_node, cur_node in zip(nodes[:-1], nodes[1:]):
            self[prev_node][cur_node] = 0.0
            self[cur_node][prev_node] = 0.0  # double-sided directed graph
        # if nodes[-1] not in self:
        #    self[nodes[-1]] = {}

    # this function has been deprecated
    # use traverse_paths(1) instead
    # def traverse(self):
    #     """
    #     Traverses the road graph and returns pairs of neighboring waypoints.
    #
    #     :rtype iterator
    #     """
    #     for node, following_nodes in self.items():
    #         for fn in following_nodes:
    #             yield (node, fn)

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
                        if node not in path:
                            yield [node] + path

    # mirror is not useful for double-directed graphs
    # def mirror(self):
    #     """
    #     Generates a mirrored graph, i.e. a graph (with the same number of nodes)
    #     whose edges are directed in the inverse direction to the given graph.
    #
    #     :return: the mirrored graph
    #     :rtype: RoadGraph
    #     """
    #     mirrored_graph = RoadGraph()
    #     for path in self.traverse_paths(length=1):
    #         start, finish = path
    #         mirrored_graph[finish][start] = self[start][finish]
    #         if start not in mirrored_graph:
    #             mirrored_graph[start] = {}
    #     return mirrored_graph

    def find_next_node(self, prev_node, cur_node):
        """
        Finds next final node with more than 1 child. Required for graph simplification algorithm.

        :param prev_node: previous node, limits the search from running backwards
        :param cur_node: current node
        :return: (total_length, new_end_node, path between cur_node and new_end_node that can be simplified)
        """
        if prev_node not in self:
            raise AttributeError("Previous node not found!" + str(prev_node))
        if cur_node not in self:
            raise AttributeError("Current node not found!" + str(cur_node))

        total_length = self[prev_node][cur_node]
        children = [ch for ch in self[cur_node] if ch != prev_node]
        path = []
        while len(children) == 1:
            if children[0] in path:
                break  # cycle!
            path.append(cur_node)
            prev_node = cur_node
            cur_node = children[0]
            children = [ch for ch in self[cur_node] if ch != prev_node]
            total_length += self[prev_node][cur_node]

        return total_length, cur_node, path

    def simplify(self, copy=True):
        """
        Simplifies graph, i.e. removes all nodes that contain only one child
        by connecting the preceding node to the following.

        :param copy: should create a copy of the graph; if False, will overwrite current graph
        :return: the simplified graph, where each node has more than 1 child, or 1 (if it is an end node).
        :rtype: RoadGraph
        """
        if copy:
            simplified_graph = deepcopy(self)
        else:
            simplified_graph = self

        for path in self.traverse_paths(length=1):
            start, finish = path

            if start not in simplified_graph or finish not in simplified_graph:
                continue  # already simplified

            total_length, next_node, path_to_remove = simplified_graph.find_next_node(start, finish)
            simplified_graph[start][next_node] = total_length
            simplified_graph[next_node][start] = total_length
            for node in path_to_remove:  # for each node in the simplification path, remove:
                if node in simplified_graph:  # if not yet removed
                    del simplified_graph[node]  # remove

            if path_to_remove:
                del simplified_graph[start][path_to_remove[0]]
                del simplified_graph[next_node][path_to_remove[-1]]

        return simplified_graph

    def dfs(self, node, ignore=None, skip_history=0):
        """
        Implements depth-first search with some modifications for RoadGraph.

        :param node: the node where the DFS should start
        :param skip_history: number of steps back in history that cannot be visited
        :param ignore: sequence of nodes that may not be revisited
        :return: list of nodes
        :rtype: iterator
        """
        # if node is None:
        #     for node in self:
        #         for path in self.dfs(node, skip_history=skip_history):
        #             yield path
        #
        # el
        if ignore is None:
            ignore = []

        if len(self[node]) == 1:
            yield [node]  # node has no children

        else:
            for child in self[node]:
                if child in ignore:
                    continue

                ignore_seq = ignore[-skip_history+1:] + [node]
                for path in self.dfs(child, skip_history=skip_history, ignore=ignore_seq):
                    yield [node] + path
