#!/usr/bin/python

import sys
from shapely.geometry import Point, Polygon

def is_float(val):
    try:
        num = float(val)
    except ValueError:
        return False
    return True


centroids = [Point((40.595231, -74.124360)), Point((40.691403, -73.906963)), Point((40.796549, -73.946916))]

for data in sys.stdin:
    data = data.strip()
    record = data.split(',')
    latitude = record[len(record)-9]
    longitude = record[len(record)-8]
    if is_float(latitude) and is_float(longitude):
        point = Point((float(latitude), float(longitude)))
        clostestCentroid = centroids[0]
        clostestDistance = point.distance(centroids[0])
        for i, centroid in enumerate(centroids):
            distance = point.distance(centroid)
            if distance < clostestDistance:
                clostestCentroid = centroid
                clostestDistance = distance
        sys.stdout.write("%s,%s\t%s,%s\n" % (clostestCentroid.x, clostestCentroid.y, point.x, point.y))
