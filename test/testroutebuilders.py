import unittest
from roadcollector import RoadCollector
from roadclassifier import VectorAngleRoadClassifier
from routebuilder import ShortestPathRouteBuilder
from roadgraph import RoadGraph


class TestRouteBuilders(unittest.TestCase):
    def setUp(self):
        # init an example graph
        self.graph = RoadGraph()
        self.graph.append_way([(0, 0), (0, 1), (0, 2), (0, 3)])
        self.graph.append_way([(0, 0), (1, 1), (1, 2)])
        self.graph.append_way([(1, 1), (2, 2)])
        self.graph.append_way([(0, 0), (2, 1)])
        self.graph.append_way([(1, 1), (3, 2), (3, 3)])
        self.graph.append_way([(3, 2), (4, 3)])

        classifier = VectorAngleRoadClassifier()
        self.classified_graph = classifier.get_classification(self.graph)

        # query = """way(47081339);out;"""
        # self.nodes = QueryRoadCollector().get_roads(query)
        # self.classes = VectorAngleRoadClassifier().get_classification(self.nodes)

    def test_build_shortest_route(self):
        rb = ShortestPathRouteBuilder()
        path = rb.build(self.classified_graph, (0, 0), (3, 3))
        for waypoint in [(0, 0), (1, 1), (3, 2), (3, 3)]:
            self.assertIn(waypoint, path, "Waypoint {} is not in the shortest path".format(waypoint))

    def test_shortest_path_is_connected(self):
        rb = ShortestPathRouteBuilder()
        path = rb.build(self.classified_graph, (0, 0), (3, 3))
        for segment in zip(path[:-1], path[1:]):
            self.assertTrue(list(segment) in self.graph.edges(),
                            "Segment {} is not available in the RoadGraph".format(str(segment)))
