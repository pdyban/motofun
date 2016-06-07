__author__ = 'missoni'


class RouteBuilder(object):
    """contructs a route along the classified list of nodes accounting for total length and fun_factor"""
    def __init__(self):
        super(self.__class__, self).__init__()

    def get_route(self, *args, **kwargs):
        """re-consider function signature here"""
        raise NotImplemented("Implement me in children!")
