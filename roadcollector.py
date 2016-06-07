__author__ = 'missoni'


class RoadCollector(object):
    def __init__(self):
        super(self.__class__, self).__init__()

    def get_roads(self, *args, **kwargs):
        raise NotImplemented("Implement me in children!")


class QueryRoadCollector(RoadCollector):
    def __init__(self):
        super(self.__class__, self).__init__()

    def get_roads(self, query):
        import overpy
        api = overpy.Overpass()
        result = api.query(query)

        nodes = []

        for way in result.ways:
            print("Name: %s" % way.tags.get("name", "n/a"))
            print("\tHighway: %s" % way.tags.get("highway", "n/a"))

            nodes_ = []
            for node in way.get_nodes(resolve_missing=True):
                nodes_.append((node.lat, node.lon,))

            nodes.append(nodes_)

        return nodes


class BoundingBoxRoadCollector(RoadCollector):
    def __init__(self):
        super(self.__class__, self).__init__()

    def get_roads(self, bbox):
        raise NotImplemented("Implement me!")
