#!/usr/bin/python

import sys

count = 0
lastKey = False
for data in sys.stdin:
    data = data.strip()
    record = data.split('\t')
    key = record[0]

    if lastKey and key != lastKey:
        sys.stdout.write("%s,%s\n" % (lastKey, count))
        lastKey = key
        count = 1
    else:
        lastKey = key
        count += 1
if lastKey:
    sys.stdout.write("%s,%s\n" % (lastKey, count))
