#! /usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.arima_model import ARMA
from util import load_data, get_mean_absolute_error, get_outlier_indices
from matplotlib.dates import datestr2num
import matplotlib.dates as mdates
from matplotlib.offsetbox import AnchoredText


def process(args):
    ## load data
    events = load_data(args["data_file"])
    train_events = [e for e in events if e[0].year < 2019]
    val_events = [e for e in events if e[0].year >= 2019]

    ## training
    train_event_counts = np.array([e[1] for e in train_events]).flatten()
    train_event_counts_first_diff = train_event_counts[1:] - train_event_counts[:-1]

    ## remove outliers
    if args["window_size"]:
        assert args["threshold"], "outlier removal threshold need to be specified"
        outlier_indices = get_outlier_indices(train_event_counts_first_diff,
                                              args["window_size"],
                                              args["threshold"])
        train_event_counts_first_diff = np.delete(train_event_counts_first_diff, outlier_indices)

    # define model
    model = ARMA(train_event_counts_first_diff, order=(args["p"], args["q"]))
    model_fit = model.fit()
    print(model_fit.summary())

    ## evaluation
    ## get evaluation data
    val_event_counts = np.array([e[1] for e in val_events]).flatten()

    ## start prediction
    prediction_diff = model_fit.predict(start=0, end=len(val_event_counts) - 1)
    prediction = [train_event_counts[-1] + prediction_diff[0]]
    for index in range(1, len(prediction_diff)):
        prediction.append(prediction[-1] + prediction_diff[index])

    ## get error
    MAE = get_mean_absolute_error(prediction, val_event_counts)

    ## set x-axis
    dates = datestr2num([e[0].strftime('%m/%d/%Y') for e in val_events])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    ## plot
    l_gt, = plt.plot(dates, val_event_counts, "b")
    l_pred, = plt.plot(dates, prediction, "r")
    ## add mae info
    plt.gca().add_artist(AnchoredText("MAE: %.2f" % MAE, loc="upper center"))
    ## add legend
    plt.legend(handles=[l_gt, l_pred], labels=['ground truth', 'prediction'], loc="best")
    ## rotate time
    plt.gcf().autofmt_xdate()

    ## set titles
    plt.title("NYPD Crime Prediction by ARMA")
    plt.ylabel("#crime events")
    plt.xlabel("crime events occurrence date")

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")
    parser.add_argument("-p", type=int, default=1, help="p value for the AR model")
    parser.add_argument("-q", type=int, default=1, help="q value for the MA model")
    parser.add_argument("-w", "--window_size", type=int, help="remove outliers window size")
    parser.add_argument("-th", "--threshold", type=int, default=2, help="outlier removal threshold")
    process(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
