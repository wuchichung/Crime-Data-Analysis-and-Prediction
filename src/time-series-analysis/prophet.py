#! /usr/bin/env python3

import argparse

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from fbprophet import Prophet
from matplotlib.dates import datestr2num
from util import load_data


def process(args):
    ## load data
    events = load_data(args["data_file"])

    ## event before 2019 for training else for validation
    train_events = [e for e in events if e[0].year < 2019]
    val_events = [e for e in events if e[0].year >= 2019]

    ## construct dataframe
    train_df = pd.DataFrame(train_events, columns=['ds', 'y'])

    ## start training
    m = Prophet(daily_seasonality=True)
    m.fit(train_df)

    ## start testing
    val_df = pd.DataFrame(val_events, columns=['ds', 'y'])
    forecast = m.predict(val_df)

    ## plot result
    ## transform date format
    dates = datestr2num([d.strftime('%m/%d/%Y') for d in val_df["ds"]])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    ## plot
    l_gt, = plt.plot(dates, val_df["y"], "b")
    l_pred, = plt.plot(dates, forecast["yhat"], "r")
    l_pred_lower, = plt.plot(dates, forecast["yhat_lower"], "g--")
    l_pred_upper, = plt.plot(dates, forecast["yhat_upper"], "c--")

    ## plot legends
    plt.legend(handles=[l_gt, l_pred, l_pred_lower, l_pred_upper],
               labels=['ground truth', 'prediction', 'prediction (lower)', 'prediction (upper)'],
               loc="best")

    plt.gcf().autofmt_xdate()
    ## set titles
    plt.title("NYPD Crime Prediction by Prophet")
    plt.ylabel("#events")
    plt.xlabel("events occurrence date")

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")

    process(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
