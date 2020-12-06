#! /usr/bin/env python3

from datetime import datetime


def load_data(data_file_path):
    events = []
    with open(data_file_path) as d_file:
        for line in d_file.readlines():
            date_str, count = line.rstrip().split("\t")
            events.append((datetime.strptime(date_str, "%Y%m%d"), int(count)))
    ## sort events by date
    events.sort(key=lambda _x: _x[0])
    return events
