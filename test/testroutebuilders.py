import unittest
from roadclassifier import VectorAngleRoadClassifier
from roadcollector import QueryRoadCollector
from routebuilder import RouteBuilder

__author__ = 'missoni'


@unittest.skip
class TestRouteBuilders(unittest.TestCase):
    def setUp(self):
        query = """way(47081339);out;"""
        self.nodes = QueryRoadCollector().get_roads(query)
        self.classes = VectorAngleRoadClassifier().get_classification(self.nodes)

    def test_build_shortest_route(self):
        rb = RouteBuilder()