#! /usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from util import load_data
from statsmodels.tsa.stattools import adfuller
from util import remove_outliers


def process(args):
    ##
    events = load_data(args["data_file"])
    event_counts = np.array([e[-1] for e in events])
    event_counts_first_diff = event_counts[1:] - event_counts[:-1]
    filtered_event_counts_first_diff = remove_outliers(event_counts_first_diff, args["window_size"])

    ##
    dftest_1 = adfuller(event_counts, autolag='AIC')
    dftest_2 = adfuller(event_counts_first_diff, autolag='AIC')
    dftest_3 = adfuller(filtered_event_counts_first_diff, autolag='AIC')
    print("adfuller", dftest_1)
    print("adfuller", dftest_2)
    print("adfuller", dftest_3)

    acf_values = acf(filtered_event_counts_first_diff)
    pacf_values = pacf(filtered_event_counts_first_diff)

    ##
    ax = plt.subplot(2, 3, 1)
    plt.plot(event_counts)
    ax.title.set_text("event count")

    ax = plt.subplot(2, 3, 2)
    plt.plot(event_counts_first_diff)
    plt.ylim(min(event_counts_first_diff), max(event_counts_first_diff))
    ax.title.set_text("event count first difference")

    ax = plt.subplot(2, 3, 3)
    plt.plot(filtered_event_counts_first_diff)
    plt.ylim(min(event_counts_first_diff), max(event_counts_first_diff))
    ax.title.set_text("event count first difference(filtered)")

    ax = plt.subplot(2, 3, 4)
    plt.bar(range(acf_values.shape[0]), acf_values)
    ax.title.set_text("ACF of event count first difference")

    ax = plt.subplot(2, 3, 5)
    plt.bar(range(pacf_values.shape[0]), pacf_values)
    ax.title.set_text("PACF of event count first difference")

    plt.show()


def main():
    parser = argparse.ArgumentParser("Tool to display ACF and PACF of timeseties data")
    parser.add_argument("data_file")
    parser.add_argument("--window_size", type=int, default=20, help="outlier removing window size")

    process(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
