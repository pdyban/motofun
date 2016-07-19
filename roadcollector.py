from roadgraph import RoadGraph
from cachedoverpassapi import CachedOverpassAPI


class RoadCollector(object):
    """
    Queries and stores list of waypoints aka roads into the internal graph format.
    """
    def __init__(self):
        super().__init__()

    def get_roads(self, *args, **kwargs):
        raise NotImplemented("Implement me in children!")


class QueryRoadCollector(RoadCollector):
    """
    Queries list of waypoints aka nodes from the online OSM DB.
    """
    def __init__(self):
        super().__init__()

    def get_roads(self, query):
        """
        Sends a query to OSM DB using short overpass syntax, stores the result in an instance of a RoadGraph.

        :return: graph that represents roads as a list of waypoints.
        :rtype: RoadGraph
        """
        api = CachedOverpassAPI('cache.sqlite')
        result = api.query(query)

        # store waypoints as a graph
        g = RoadGraph()

        for way in result:
            g.append_way(way)

        return g


class BoundingBoxRoadCollector(RoadCollector):
    def __init__(self):
        super().__init__()

    def get_roads(self, bbox):
        raise NotImplemented("Implement me!")
