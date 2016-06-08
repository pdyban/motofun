import unittest
from roadcollector import *
from roadclassifier import *
from routebuilder import *


class TestRoadCollectors(unittest.TestCase):
    def test_query_road_by_id(self):
        query = """way(47081339);out;"""
        roads = QueryRoadCollector().get_roads(query)
        self.assertEqual(len(roads), 1)
        self.assertEqual(len(roads[0]), 57)

    def test_query_two_roads(self):
        query = """(way(161468888);way(47081339););
                (._;>;);
                out;"""
        roads = QueryRoadCollector().get_roads(query)
        self.assertEqual(len(roads), 2)
        self.assertEqual(len(roads[0]), 57)
        self.assertEqual(len(roads[1]), 100)


class TestRoadClassifiers(unittest.TestCase):
    def setUp(self):
        query = """way(47081339);out;"""
        self.nodes = QueryRoadCollector().get_roads(query)

    def test_vector_angle_classifier(self):
        graph = VectorAngleRoadClassifier().get_classification(self.nodes)
        self.assertEqual(len(graph), 56)  # consists of list of road points aka nodes
        self.assertIsInstance(graph, dict)
        # for node in graph:
        #     for other_node in graph[node]:
        #         print('+ %s -> %s : %.2f' % (node, other_node, graph[node][other_node]))

        # self.assertEqual(len(c[0]), len(self.nodes))  # list of road points should not change due to classification
        # self.assertEqual(len(c[1]), len(c[0]))  # fun factor list should contain a value for each road point


@unittest.skip
class TestRouteBuilders(unittest.TestCase):
    def setUp(self):
        query = """way(47081339);out;"""
        self.nodes = QueryRoadCollector().get_roads(query)
        self.classes = VectorAngleRoadClassifier().get_classification(self.nodes)

    def test_build_shortest_route(self):
        rb = RouteBuilder()


if __name__ == '__main__':
    unittest.main()
