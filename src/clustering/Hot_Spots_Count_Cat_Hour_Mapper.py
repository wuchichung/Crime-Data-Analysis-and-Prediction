#!/usr/bin/python

import sys
import numpy as np
from shapely.geometry import Point, Polygon


def is_float(val):
    try:
        num = float(val)
    except ValueError:
        return False
    return True


bottomLeft = (40.446927, -74.365192)
topLeft = (40.938658, -74.365192)
bottomRight = (40.446927, -73.641071)
topRight = (40.938658, -73.641071)

cols = np.linspace(bottomLeft[1], bottomRight[1], num=100)
rows = np.linspace(bottomLeft[0], topLeft[0], num=100)

polygonList = []
for i, row in enumerate(rows):
    for j, col in enumerate(cols):
        if i+1 < len(rows) and j+1 < len(cols):
            coords = [(rows[i], cols[j]), (rows[i], cols[j+1]),
                      (rows[i+1], cols[j+1]), (rows[i+1], cols[j])]
            polygon = Polygon(coords)
            polygonList.append(polygon)

for data in sys.stdin:
    data = data.strip()
    record = data.split(',')
    latitude = record[len(record)-9]
    longitude = record[len(record)-8]
    category = record[len(record)-24]
    time = record[2]
    if is_float(latitude) and is_float(longitude):
        point = Point((float(latitude), float(longitude)))
        for p in polygonList:
            if point.within(p):
                sys.stdout.write("%s,%s,%s,%s\t%s\n" %
                                 (p.centroid.x, p.centroid.y, time[:2], category, 1))
                break
