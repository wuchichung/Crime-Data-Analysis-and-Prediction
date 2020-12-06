#! /usr/bin/env python3

import sys

curr_event_date = None
curr_num_event_count = 0

for line in sys.stdin:
    ## parse line
    event_date, _ = line.strip().split("\t")

    ##
    if event_date == curr_event_date:
        curr_num_event_count += 1
    else:
        if curr_event_date is not None:
            print("%s\t%d" % (curr_event_date, curr_num_event_count))
        curr_event_date = event_date
        curr_num_event_count = 1

if curr_event_date is not None:
    print("%s\t%d" % (curr_event_date, curr_num_event_count))
