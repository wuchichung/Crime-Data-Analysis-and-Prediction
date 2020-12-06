#! /usr/bin/env python3


import sys

for line in sys.stdin:
    ## parse line
    line = line.strip()
    data = line.split(",")

    ## ignore header
    if data[1] == "CMPLNT_FR_DT":
        continue

    ## do some check, as CMPLNT_FR_DT is empty for some entries
    tmp = data[1].split("/")
    if len(tmp) == 3:
        ## convert time format from month/date/year -> year/month/date
        m, d, y = tmp
        print("%s%s%s\t1" % (y, m, d))
