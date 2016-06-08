__author__ = 'missoni'

import numpy as np


class RoadClassifier(object):
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

    def get_classification(self, nodes):
        """not finished yet"""

        def calculate_angle(p0, p1, p2):
            """
            Calculates angle between (p0,p1) and (p0,p2)
            """
            import numpy as np
            a = np.array((p0[0]-p1[0],p0[1]-p1[1]))
            b = np.array((p0[0]-p2[0],p0[1]-p2[1]))
            return np.arccos(np.dot(a, b)/np.linalg.norm(a)/np.linalg.norm(b))

        def convert_to_meters(p0, p1):
            """
            Converts distance between 2 2D points in geo coordinates to meters.
            """
            def to_radians(angle):
                from math import pi
                return angle*pi/180.0

            from math import sin, cos, pi, sqrt, atan2
            lat1, lon1 = p0
            lat2, lon2 = p1
            R = 6371 # km
            dLat = to_radians(lat2-lat1)
            dLon = to_radians(lon2-lon1)
            lat1 = to_radians(lat1)
            lat2 = to_radians(lat2)

            a = sin(dLat/2) * sin(dLat/2) + sin(dLon/2) * sin(dLon/2) * cos(lat1) * cos(lat2)
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            d = R * c
            return d

        points = []
        fun_classes = []
        for path in nodes:
            intensity = [0]*len(path)
            total_spass = 0.0
            total_distance = 0.0
            for index in range(len(path)-2):
                p0 = np.array(path[index],dtype=np.float)
                p1 = np.array(path[index+1],dtype=np.float)
                p2 = np.array(path[index+2],dtype=np.float)
                # intens = np.linalg.norm(p0-p2)/(np.linalg.norm(p0-p1) + np.linalg.norm(p2-p1))
                # intens = approximate_parabole(p0,p1,p2)
                intens = calculate_angle(p0,p1,p2)
                intensity[index+1] = intens
                points.append([p1, intens])
                total_spass += intens
                # print(convert_to_meters(p0, p1))
                total_distance += convert_to_meters(p0, p1)

            if total_distance < 0.01:
                continue

            # print('total ' + str(total_spass/total_distance))
            total_spass /= total_distance
            total_spass *= 1000.0
            if total_spass > 10:
                c = 'black'
            elif total_spass > 6:
                c = 'red'
            elif total_spass > 3:
                c = 'green'
            elif total_spass > 1:
                c = 'blue'
            else:
                c = 'gray'
            fun_classes.append(c)

        return (nodes, fun_classes)


class TriangleRoadClassifier(RoadClassifier):
    def __init__(self):
        super().__init__()

    def get_classification(self, nodes):
        raise NotImplemented("Implement me!")
