__author__ = 'missoni'

import unittest
from roadcollector import *


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


if __name__ == '__main__':
    unittest.main()
