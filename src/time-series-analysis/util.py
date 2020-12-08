#! /usr/bin/env python3

from datetime import datetime

import numpy as np


def load_data(data_file_path):
    events = []
    with open(data_file_path) as d_file:
        for line in d_file.readlines():
            date_str, count = line.rstrip().split("\t")
            events.append((datetime.strptime(date_str, "%Y%m%d"), int(count)))
    ## sort events by date
    events.sort(key=lambda _x: _x[0])
    return events


def get_mean_absolute_error(ground_truth, prediction):
    return np.mean(abs(np.array(ground_truth) - np.array(prediction)))


def get_outlier_indices(data, window_size, thresh=3):
    ## get outlier index
    indices = []
    for start_index in range(0, len(data), int(0.5 * window_size)):
        ## get stop index
        stop_index = min(len(data), start_index + window_size)
        ## calculate the window mean and standard deviation
        std = np.std(np.array(data[start_index: stop_index]))
        mean = np.mean(np.array(data[start_index: stop_index]))
        ## get the threshold relative to standard deviation
        threshold = thresh * std
        ## append outlier indices
        indices.extend([i for i in range(start_index, stop_index) if abs(data[i] - mean) > threshold])

    return sorted(list(set(indices)))
