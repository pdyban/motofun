import unittest
from roadcollector import *
from roadclassifier import *
from routebuilder import *
from roadgraph import *


class TestRoadGraph(unittest.TestCase):
    def setUp(self):
        # init an example graph
        self.graph = RoadGraph()
        self.graph.append_way([(0, 0), (0, 1), (0, 2), (0, 3)])
        self.graph.append_way([(0, 0), (1, 1), (1, 2)])
        self.graph.append_way([(1, 1), (2, 2)])
        self.graph.append_way([(0, 0), (2, 1)])
        self.graph.append_way([(1, 1), (3, 2), (3, 3)])
        self.graph.append_way([(3, 2), (4, 3)])

    def test_traverse_two_segment_paths_from_source(self):
        """
        Traverse all paths that contain exactly two segments, starting from a given source node.
        """
        ipaths = self.graph.traverse_paths(node=(0, 0), length=2)
        paths = [path for path in ipaths]

        self.assertIn([(0, 0), (0, 1), (0, 2)], paths)
        self.assertIn([(0, 0), (1, 1), (1, 2)], paths)
        self.assertIn([(0, 0), (1, 1), (3, 2)], paths)
        self.assertIn([(0, 0), (1, 1), (2, 2)], paths)
        self.assertEqual(len(paths), 4)

    def test_traverse_all_two_segment_paths(self):
        """
        Traverse all paths in a graph that contain two segments.
        """
        ipaths = self.graph.traverse_paths(length=2)
        paths = [path for path in ipaths]

        self.assertIn([(0, 1), (0, 2), (0, 3)], paths)
        self.assertIn([(0, 0), (0, 1), (0, 2)], paths)
        self.assertIn([(0, 0), (1, 1), (1, 2)], paths)
        self.assertIn([(0, 0), (1, 1), (3, 2)], paths)
        self.assertIn([(0, 0), (1, 1), (2, 2)], paths)
        self.assertIn([(1, 1), (3, 2), (3, 3)], paths)
        self.assertIn([(1, 1), (3, 2), (4, 3)], paths)
        self.assertEqual(len(paths), 7)

    def test_traverse_all_three_segment_paths(self):
        """
        Traverse all paths in a graph that contain three segments.
        """
        ipaths = self.graph.traverse_paths(length=3)
        paths = [path for path in ipaths]  # convert iterator to list

        self.assertIn([(0, 0), (0, 1), (0, 2), (0, 3)], paths)
        self.assertIn([(0, 0), (1, 1), (3, 2), (3, 3)], paths)
        self.assertIn([(0, 0), (1, 1), (3, 2), (4, 3)], paths)
        self.assertEqual(len(paths), 3)

    def test_traverse_all_one_segment_paths(self):
        """
        Traverse all paths that contain one segments, i.e. all paths in a graph that connect two waypoints.
        """
        ipaths = self.graph.traverse_paths()
        paths = [path for path in ipaths]  # convert iterator to list

        self.assertIn([(0, 1), (0, 2)], paths)
        self.assertIn([(3, 2), (3, 3)], paths)
        self.assertIn([(3, 2), (4, 3)], paths)
        self.assertIn([(0, 0), (0, 1)], paths)
        self.assertIn([(0, 0), (1, 1)], paths)
        self.assertIn([(0, 0), (2, 1)], paths)
        self.assertIn([(0, 2), (0, 3)], paths)
        self.assertIn([(1, 1), (1, 2)], paths)
        self.assertIn([(1, 1), (3, 2)], paths)
        self.assertIn([(1, 1), (2, 2)], paths)
        self.assertEqual(len(paths), 10)


class TestRoadCollectors(unittest.TestCase):
    def test_query_road_by_id(self):
        query = """way(47081339);out;"""
        roads = QueryRoadCollector().get_roads(query)
        self.assertEqual(len(roads), 56)

    def test_query_two_roads(self):
        query = """(way(161468888);way(47081339););
                (._;>;);
                out;"""
        roads = QueryRoadCollector().get_roads(query)
        self.assertEqual(len(roads), 155)


class TestRoadClassifiers(unittest.TestCase):
    def setUp(self):
        query = """way(47081339);out;"""
        self.road_graph = QueryRoadCollector().get_roads(query)

    def test_vector_angle_classifier(self):
        graph = VectorAngleRoadClassifier().get_classification(self.road_graph)
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
