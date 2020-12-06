#!/usr/bin/python

import sys

count = 0
lastKey = False
xSum = 0.0
ySum = 0.0
for data in sys.stdin:
    data = data.strip()
    record = data.split('\t')
    coordinate = record[0]
    point = record[1]

    if lastKey and coordinate != lastKey:
        sys.stdout.write("%s,%s\t%s\n" % (xSum/count, ySum/count, count))
        lastKey = coordinate
        pointCoordinate = point.split(',')
        xSum = float(pointCoordinate[0])
        ySum = float(pointCoordinate[1])
        count = 1
    else:
        lastKey = coordinate
        count += 1
        pointCoordinate = point.split(',')
        xSum += float(pointCoordinate[0])
        ySum += float(pointCoordinate[1])
if lastKey:
    sys.stdout.write("%s,%s\t%s\n" % (xSum/count, ySum/count, count))
