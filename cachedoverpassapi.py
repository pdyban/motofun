import overpy
import sqlite3
import pickle
from roadgraph import RoadGraphX


class CachedOverpassAPI(overpy.Overpass):
    """
    Cached interface to online Overpass API. Stores queries' results in cache.
    """
    def __init__(self, dbfile, verbose=False, read_chunk_size=None,
                 # delete_on_destroyed=False
                 ):
        """
        :param dbfile: path to dbfile file that stores the cache
        :param verbose: should print debugging messages
        :param read_chunk_size: see overpy.Overpass.__init__()
        :param delete_on_destroyed: should delete sqlite file when cache is destroyed
        """
        super().__init__(read_chunk_size)

        self.dbfile = dbfile
        self.conn = None
        self.cursor = None  # database cursor for executing queries
        self.verbose = verbose
        # self.delete_on_destroyed = delete_on_destroyed

        self.print_verbose("Creating new cached DB interface")

        self.connect_to_db(self.dbfile)

    def __del__(self):
        self.print_verbose("Destroying cached DB interface")
        self.disconnect_from_db(self.dbfile)
        # if self.delete_on_destroyed:
        #     self.print_verbose("Removing cache DB file", self.dbfile)
        #     from warnings import warn
        #     warn('''Cache DB file at {} cannot be deleted. Not yet implemented due to concurrency issues.''' \
        #          .format(self.dbfile))
        #     # os.remove(self.dbfile)

    def print_verbose(self, *args):
        """
        Prints a message only if init'd in verbose mode.

        :param args: the variable-length list of arguments to print
        """
        if self.verbose:
            print(*args)

    def connect_to_db(self, dbfile):
        """
        Connects to cache DB given by dbfile.

        :param dbfile: path to dbfile (sqlite)
        """
        self.print_verbose("Connecting to local cache DB")
        self.conn = sqlite3.connect(dbfile)
        self.create_empty_cache()  # will quietly do nothing if cache table already exists

    def disconnect_from_db(self, dbfile):
        self.print_verbose("Disconnecting from local cache DB")
        self.conn.close()

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

    def query(self, query):
        """
        Executes the query and stores the result in the cache DB

        :todo: design a way to convert overpass results to json
        """
        result = self.query_cache(query)
        if result is not None:
            return result

        self.print_verbose('Processing query online', query)
        result = super().query(query)
        result.api = super()  # important for resolution of missing nodes
        processed_result = self.process_result(result)
        self.store_to_cache(query, processed_result)
        return processed_result

    def query_cache(self, query):
        """
        Executes a query in the cache DB.

        :return: the road graph, if available; otherwise, None
        :rtype: RoadGraphX
        """
        self.print_verbose('Query cache', query)
        cursor = self.conn.cursor()
        result = cursor.execute("SELECT Result FROM CachedQueries WHERE Query=?", (query,))

        binary_result = result.fetchone()
        if binary_result is None:
            self.print_verbose('Returning from Overpass online DB')
            return None

        self.print_verbose('Returning from local cache')
        return pickle.loads(binary_result[0])

    def store_to_cache(self, query, result):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO CachedQueries(Query, Result) VALUES (?,?);", (
            query, pickle.dumps(result),))
        self.conn.commit()

    def process_result(self, result):
        """
        Processed the result from overpass format to a Python standard format.
        """
        # nodes = []
        graph = RoadGraphX()
        for way in result.ways:
            nodes_ = []
            # print(way.tags.get('maxspeed', None), way.tags.get('name', None))
            for node in way.get_nodes(resolve_missing=True):
                nodes_.append((node.lon, node.lat,))

            graph.append_road(way.tags, nodes_)
            # nodes.append(nodes_)
        return graph

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
