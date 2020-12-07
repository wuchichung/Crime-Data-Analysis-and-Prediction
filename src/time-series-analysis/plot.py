#! /usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from util import load_data
from statsmodels.tsa.stattools import adfuller
from util import get_outlier_indices


def process(args):
    ##
    events = load_data(args["data_file"])

    event_counts = np.array([e[-1] for e in events])
    event_counts_outliers = get_outlier_indices(event_counts, args["window_size"])

    event_counts_first_diff = event_counts[1:] - event_counts[:-1]
    event_counts_first_diff_outliers = get_outlier_indices(event_counts_first_diff, args["window_size"])

    ##
    ax = plt.subplot(2, 1, 1)
    plt.plot(event_counts)
    plt.scatter(event_counts_outliers, event_counts[event_counts_outliers], s=80, facecolors='none', edgecolors='r')
    ax.title.set_text("crime event count")

    ax = plt.subplot(2, 1, 2)
    plt.plot(event_counts_first_diff)
    plt.scatter(event_counts_first_diff_outliers,
                event_counts_first_diff[event_counts_first_diff_outliers], s=80, facecolors='none', edgecolors='r')

    plt.ylim(min(event_counts_first_diff), max(event_counts_first_diff))
    ax.title.set_text("first difference of crime event count ")

    #
    plt.show()


def main():
    parser = argparse.ArgumentParser("Tool to display ACF and PACF of timeseties data")
    parser.add_argument("data_file")
    parser.add_argument("-w", "--window_size", type=int, default=20, help="outlier removing window size")

    process(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
