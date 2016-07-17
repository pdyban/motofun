import unittest
from cachedoverpassapi import CachedOverpassAPI
import os


class TestCachedAPI(unittest.TestCase):
    def setUp(self):
        self.api = CachedOverpassAPI('cache.sqlite')
        self.api.clear_cache()

    def tearDown(self):
        os.remove('cache.sqlite')

    def test_cache_is_empty(self):
        self.api.clear_cache()
        self.assertEqual(self.api.cache_is_empty(), True)

    # @todo: design a way to convert overpass results to json
    @unittest.skip
    def test_cache_stores_queries(self):
        query = "way(47081339);out;"
        res = self.api.query(query)
        self.assertEqual(self.api.cache_is_empty(), False)
        self.assertNotEqual(self.api.query_cache(query), None)
        self.assertEqual(len(self.api.query_cache(query).ways), len(res.ways))

    def test_cache_stores_query_only_once(self):
        query = "way(47081339);out;"
        self.api.query(query)
        size1 = self.api.get_cache_size()
        self.api.query(query)
        size2 = self.api.get_cache_size()
        self.assertEqual(size1, size2)

    def test_returns_none_if_query_not_in_cache(self):
        self.api.clear_cache()
        query = "way(47081339);out;"
        self.assertIs(self.api.query_cache(query), None)
