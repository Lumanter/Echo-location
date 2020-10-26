import math
from point import Point

def find_angle(pointA, pointB): # given clockwise in radians
    x1, y1 = pointA.x, pointA.y
    x2, y2 = pointB.x, pointB.y
    angle = math.atan2(y2-y1, x2-x1)
    if angle < 0:
        angle += math.pi * 2
    return angle



def ray_segment_intersection_point(ori, dir, p1, p2):
    v1 = ori - p1 #se definen los 3 vectores
    v2 = p2 - p1
    v3 = Point(-dir.y, dir.x)

    dot = v2.dot(v3) #se calcula el denominador
    if abs(dot) < 0.000001: #si dot es 0, el vector y el segmento son paralelos
        return None           #y no hay interseccion

    t1 = v2.cross(v1) / dot #t1 es la distancia del origen hasta la interseccion
    t2 = v1.dot(v3) / dot #t2 indica si la interseccion queda dentro del segmento

    if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
        x_intersect = ori.x + dir.x*t1
        y_intersect = ori.y + dir.y*t1
        intersection_point = Point(x_intersect, y_intersect)
        return intersection_point
    else:
        return None