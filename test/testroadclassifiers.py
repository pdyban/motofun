import unittest
from roadclassifier import VectorAngleRoadClassifier
from roadcollector import QueryRoadCollector

__author__ = 'missoni'


class TestRoadClassifiers(unittest.TestCase):
    def setUp(self):
        query = """way(47081339);out;"""
        self.road_graph = QueryRoadCollector().get_roads(query)

    def test_vector_angle_classifier(self):
        graph = VectorAngleRoadClassifier().apply(self.road_graph)
        self.assertEqual(len(graph), 57)  # consists of list of road points aka nodes
        self.assertIsInstance(graph, dict)
        # for node in graph:
        #     for other_node in graph[node]:
        #         print('+ %s -> %s : %.2f' % (node, other_node, graph[node][other_node]))

        # self.assertEqual(len(c[0]), len(self.nodes))  # list of road points should not change due to classification
        # self.assertEqual(len(c[1]), len(c[0]))  # fun factor list should contain a value for each road point