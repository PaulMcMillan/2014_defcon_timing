import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats, interpolate, signal
import random
from itertools import chain

import results

def choose_points(qr_list):
    return [d.total_response() for d in qr_list]

def filter_points(qr_list, filtdata):
    return [d.total_response() - filtdata[d.response[0]] for d in qr_list]


def check_data(data):
    """ graph the values """
    tsdata = data.all_as_timeseries()
    filtdata = dict(zip(
        [x.response[0] for x in tsdata],
        signal.medfilt(choose_points(tsdata), kernel_size=55)))
#    plt.plot([x.response[0] for x in tsdata], label='boo')
    for key, val in data.items():
        plt.plot([x.response[0] for x in val],
                 sorted(filter_points(val, filtdata)),
#                 '.',
                 alpha=0.5,
                 label=str(key),
                 )
    plt.legend()
    plt.show()

data = results.read_data(bucket=r'^/api/\w{5}(\w)\w{4}/config$',
                         filename='data/out.parsed')


check_data(data)
