import heapq
from math import log


class RouteBuilder(object):
    """contructs a route along the classified list of nodes accounting for total length and fun_factor"""
    def __init__(self):
        super().__init__()

    def build(self, graph, *args, **kwargs):
        """
        Constructs a route in the given graph provided the options.

        :param graph: the graph that represents the road system
        :type graph: RoadGraph
        :return: list of waypoints that constitute the route
        """
        raise NotImplemented("Implement me in children!")


class ShortestPathRouteBuilder(RouteBuilder):
    """
    Constructs the shortest path in the road graph.
    """
    def build(self, graph, source, target):
        """
        Constructs the shortest path in the given graph
        that runs from the source to the target node.

        :param graph: the graph that represents the road system
        :type graph: RoadGraph
        :return: list of waypoints that constitute the shortest path
        """
        return self.shortestPath(graph, source, target)

    def shortestPath(self, G, start, end):
        """
        Dijkstra's algorithm for shortest paths
        David Eppstein, UC Irvine, 4 April 2002
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228

        :param G: the graph in dict(dict) format
        :param start: the starting node aka the source
        :param end: the finish node aka the sink
        :return: list of waypoints that constitute the shortest path
        """
        def flatten(L):       # Flatten linked list of form [0,[1,[2,[]]]]
            while len(L) > 0:
                yield L[0]
                L = L[1]

        q = [(0, start, ())]  # Heap of (cost, path_head, path_rest).
        visited = set()       # Visited vertices.
        while True:
            (cost, v1, path) = heapq.heappop(q)
            if v1 not in visited:
                visited.add(v1)
                if v1 == end:
                    return list(flatten(path))[::-1] + [v1]
            path = (v1, path)
            for (v2, cost2) in G[v1].items():
                if v2 not in visited:
                    heapq.heappush(q, (cost + cost2, v2, path))
