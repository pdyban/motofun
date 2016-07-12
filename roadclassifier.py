__author__ = 'missoni'

import numpy as np
from math import pi


class RoadClassifier(object):
    """
    Converts list of nodes to a graph, computes a score for each edge in the graph.
    """
    def __init__(self):
        super().__init__()

    def get_classification(self, nodes):
        """
        Classifies list of nodes into fun classes.

        @todo: re-consider function signature here, perhaps replace nodes with a specific class
        """
        raise NotImplemented("Implement me in children!")


class VectorAngleRoadClassifier(RoadClassifier):
    def __init__(self):
        super().__init__()

    def get_classification(self, road_graph):
        """not finished yet"""

        def calculate_angle(p0, p1, p2):
            """
            Calculates angle between (p0,p1) and (p0,p2)
            """
            a = np.array((p0[0]-p1[0], p0[1]-p1[1]))
            b = np.array((p0[0]-p2[0], p0[1]-p2[1]))
            return np.arccos(np.dot(a, b)/np.linalg.norm(a)/np.linalg.norm(b))

        def calculate_angle_per_distance(p0, p1, p2):
            """
            Calculates angle per distance feature.

            Distance between p0 and p1, because the feature will be attached to that edge.
            """
            feature = calculate_angle(p0, p1, p2)
            a = np.array((p0[0]-p1[0], p0[1]-p1[1]))
            feature /= np.linalg.norm(a)
            return feature

        def to_radians(angle):
            return angle*pi/180.0

        def to_degrees(angle):
            return angle*180.0/pi

        def convert_to_meters(p0, p1):
            """
            Converts distance between 2 2D points in geo coordinates to meters.
            """
            from math import sin, cos, sqrt, atan2
            lat1, lon1 = p0
            lat2, lon2 = p1
            R = 6371 # km

            lon1 = np.float(lon1)
            lon2 = np.float(lon2)
            lat1 = np.float(lat1)
            lat2 = np.float(lat2)

            dLat = to_radians(lat2-lat1)
            dLon = to_radians(lon2-lon1)
            lat1 = to_radians(lat1)
            lat2 = to_radians(lat2)

            a = sin(dLat/2)**2 + sin(dLon/2)**2 * cos(lat1) * cos(lat2)
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            d = R * c
            return d * 1000

        for path in road_graph.traverse_paths(length=2):
            p0, p1, p2 = path
            p0_float = np.array(p0, dtype=np.float)
            p1_float = np.array(p1, dtype=np.float)
            p2_float = np.array(p2, dtype=np.float)
            angle = calculate_angle(p0_float, p1_float, p2_float)
            if to_degrees(angle) < 5:
                angle = 0
            elif to_degrees(angle) > 40:
                angle = 0
            # if to_degrees(angle) > 40 or to_degrees(angle) < 10:
            #     fun_factor = 0
            # else:
            #     fun_factor = 1

            fun_factor = to_degrees(angle)

            road_graph[p0][p1] = fun_factor

        return road_graph


class TriangleRoadClassifier(RoadClassifier):
    def __init__(self):
        super().__init__()

    def get_classification(self, nodes):
        raise NotImplemented("Implement me!")
