#!/usr/bin/python

import sys

count = 0
lastKey = False
for data in sys.stdin:
    data = data.strip()
    record = data.split('\t')
    coordinate = record[0];
    
    if lastKey and coordinate != lastKey:
        sys.stdout.write("%s,%s\n" %(lastKey, count))
        lastKey = coordinate
        count = 1
    else:
        lastKey = coordinate
        count += 1
if lastKey:
    sys.stdout.write("%s,%s\n" %(lastKey, count))
