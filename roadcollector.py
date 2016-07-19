from roadgraph import RoadGraph
from cachedoverpassapi import CachedOverpassAPI


class RoadCollector(object):
    def __init__(self):
        super().__init__()

    def get_roads(self, *args, **kwargs):
        raise NotImplemented("Implement me in children!")


class QueryRoadCollector(RoadCollector):
    def __init__(self):
        super().__init__()

    def get_roads(self, query):
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
