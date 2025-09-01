import math

class Math:
    @staticmethod
    def rect_area(w, h): return w * h
    @staticmethod
    def circle_area(r): return math.pi * r * r
    @staticmethod
    def distance(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
    @staticmethod
    def polygon_area(pts):
        return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] -
                       pts[(i + 1) % len(pts)][0] * pts[i][1]
                       for i in range(len(pts))) / 2)