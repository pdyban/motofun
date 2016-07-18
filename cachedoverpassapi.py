import overpy
import sqlite3
import pickle


class CachedOverpassAPI(overpy.Overpass):
    def __init__(self, dbfile, read_chunk_size=None):
        """
        :param dbfile: path to dbfile file that stores the cache
        """
        super().__init__(read_chunk_size)

        self.conn = None
        self.cursor = None  # database cursor for executing queries

        self.connect_to_db(dbfile)

    def clear_cache(self):
        """
        Removes all cached items from cache DB.
        """
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE CachedQueries")
        self.create_empty_cache()

    def create_empty_cache(self):
        """
        Creates tables for storing cached items in the DB.
        """
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS CachedQueries (Query, Result )")

    def connect_to_db(self, dbfile):
        """
        Connects to cache DB given by dbfile.

        :param dbfile: path to dbfile (sqlite)
        """
        self.conn = sqlite3.connect(dbfile)
        self.create_empty_cache()  # will quietly do nothing if cache table already exists

    def query(self, query):
        """
        Executes the query and stores the result in the cache DB

        :todo: design a way to convert overpass results to json
        """
        result = self.query_cache(query)
        if result is not None:
            return result

        # debugging
        # return overpy.Result()
        result = super().query(query)
        self.store_to_cache(query, result)
        return result

    def store_to_cache(self, query, result):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO CachedQueries(Query, Result) VALUES (?,?);", (
            query, pickle.dumps(result),))
        self.conn.commit()

    def query_cache(self, query):
        """
        Executes a query in the cache DB.

        :return: result
        :rtype: ??
        """
        cursor = self.conn.cursor()
        result = cursor.execute("SELECT Result FROM CachedQueries WHERE Query=?", (query,))

        binary_result = result.fetchone()
        if binary_result is None:
            return None

        return pickle.loads(binary_result[0])

    def cache_is_empty(self):
        """
        Checks if the cache DB is empty.
        """
        return self.get_cache_size() == 0

    def get_cache_size(self):
        """
        Returns number of queries stored in the cache DB.
        """
        cursor = self.conn.cursor()
        result = cursor.execute("SELECT COUNT(*) FROM CachedQueries")
        return int(result.fetchone()[0])
