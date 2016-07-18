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

        nodes = []

        # store waypoints as a graph
        g = RoadGraph()

        for way in result.ways:
            # print("Name: %s" % way.tags.get("name", "n/a"))
            # print("\tHighway: %s" % way.tags.get("highway", "n/a"))

            nodes_ = []
            for node in way.get_nodes(resolve_missing=True):
                nodes_.append((node.lat, node.lon,))

            nodes.append(nodes_)

            # store waypoints as a graph
            g.append_way(nodes_)

        return g


class BoundingBoxRoadCollector(RoadCollector):
    def __init__(self):
        super().__init__()

    def get_roads(self, bbox):
        raise NotImplemented("Implement me!")
