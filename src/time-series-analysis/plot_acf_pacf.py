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
    event_counts_first_diff = event_counts[1:] - event_counts[:-1]

    acf_values = acf(event_counts_first_diff)
    pacf_values = pacf(event_counts_first_diff)

    ax = plt.subplot(2, 1, 1)
    plt.bar(range(acf_values.shape[0]), acf_values)
    ax.title.set_text("ACF of creaxon event count first difference")

    ax = plt.subplot(2, 1, 2)
    plt.bar(range(pacf_values.shape[0]), pacf_values)
    ax.title.set_text("PACF of creaoxn event count first difference")

    plt.show()


def main():
    parser = argparse.ArgumentParser("Tool to display ACF and PACF of timeseties data")
    parser.add_argument("data_file")

    process(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
