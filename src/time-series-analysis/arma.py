#! /usr/bin/env python3

import argparse
import matplotlib.pyplot  as plt
from statsmodels.tsa.arima_model import ARMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import statsmodels.tsa.stattools as st

from util import load_data


def process(args):
    ##
    events = load_data(args["data_file"])
    ##
    event_counts = [e[1] for e in events]

    order = st.arma_order_select_ic(event_counts, max_ar=5, max_ma=5, ic=['aic', 'bic', 'hqic'])

    model = ARMA(event_counts, order=order.bic_min_order)
    result_arma = model.fit(disp=-1, method='css')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")
    process(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
