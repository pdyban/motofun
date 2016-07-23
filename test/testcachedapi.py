import unittest
from cachedoverpassapi import CachedOverpassAPI


class TestCachedAPI(unittest.TestCase):
    def setUp(self):
        self.api = CachedOverpassAPI('cache.sqlite', verbose=True, delete_on_destroyed=True)
        self.api.clear_cache()

    def tearDown(self):
        # may remove the sqlite, if necessary
        # os.remove('cache.sqlite')
        pass

    def test_cache_is_empty(self):
        self.api.clear_cache()
        self.assertEqual(self.api.cache_is_empty(), True)

    def test_cache_stores_queries(self):
        query = "way(47081339);out;"
        res = self.api.query(query)
        self.assertEqual(self.api.cache_is_empty(), False)
        self.assertNotEqual(self.api.query_cache(query), None)
        self.assertEqual(self.api.query_cache(query).num_edges(), res.num_edges())
        self.assertEqual(self.api.query_cache(query).num_nodes(), res.num_nodes())

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

    def test_cache_ignores_newlines(self):
        self.api.clear_cache()
        query = """way(47081339);
                out;"""
        res = self.api.query(query)
        self.assertIsNotNone(res)
        self.assertIsNot(self.api.query_cache(query), None)
        self.assertIsNot(self.api.query_cache(query.replace('\n', '')), None)

