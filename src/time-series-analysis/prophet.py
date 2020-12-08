#! /usr/bin/env python3

import argparse

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from fbprophet import Prophet
from matplotlib.dates import datestr2num
from matplotlib.offsetbox import AnchoredText
from util import load_data, get_mean_absolute_error, get_outlier_indices

import numpy as np


def process(args):
    ## load data
    events = load_data(args["data_file"])

    ## event before 2019 for training else for validation
    train_events = [e for e in events if e[0].year < 2019]
    val_events = [e for e in events if e[0].year >= 2019]

    ## remove outliers
    if args["window_size"]:
        train_events_counts = [e[-1] for e in train_events]
        outlier_indices = get_outlier_indices(train_events_counts,
                                              args["window_size"],
                                              args["threshold"])

        for index in reversed(outlier_indices):
            train_events.pop(index)

    ## construct dataframe
    train_df = pd.DataFrame(train_events, columns=['ds', 'y'])
    val_df = pd.DataFrame(val_events, columns=['ds', 'y'])

    ## init model
    if args["growth"] == "linear":
        m = Prophet(n_changepoints=args["n_changepoints"],
                    changepoint_range=args["changepoint_range"],
                    growth=args["growth"]
                    )
    elif args["growth"] == "logistic":
        m = Prophet(growth=args["growth"])
        train_df["cap"] = train_df["y"].max()
        val_df["cap"] = train_df["y"].max()
    else:
        raise ValueError("Unknow trend function type")

    ## start training
    m.fit(train_df)

    ## start testing

    forecast = m.predict(val_df)

    ##
    MAE = get_mean_absolute_error(forecast["yhat"], val_df["y"])

    ## plot result
    ## transform date format
    dates = datestr2num([d.strftime('%m/%d/%Y') for d in val_df["ds"]])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    ## plot
    l_gt, = plt.plot(dates, val_df["y"], "b")
    l_pred, = plt.plot(dates, forecast["yhat"], "r")

    ## show MAE
    plt.gca().add_artist(AnchoredText("MAE: %.2f" % MAE, loc="upper center"))

    ## plot legends
    plt.legend(handles=[l_gt, l_pred],
               labels=['ground truth', 'prediction'],
               loc="best")
    ## rotate time
    plt.gcf().autofmt_xdate()
    ## set titles
    plt.title("NYPD Crime Prediction by Prophet")
    plt.ylabel("#events")
    plt.xlabel("events occurrence date")

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")
    parser.add_argument("-g", "--growth", default="linear", help="setting of the growth function")
    parser.add_argument("-n_cpts", "--n_changepoints", type=int, default=25, help="number of change point")
    parser.add_argument("-cpt_range", "--changepoint_range", type=float, default=0.8, help="change point range")
    parser.add_argument("-w", "--window_size", type=int, help="remove outliers window size")
    parser.add_argument("-th", "--threshold", type=int, default=2, help="outlier removal threshold")

    process(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
