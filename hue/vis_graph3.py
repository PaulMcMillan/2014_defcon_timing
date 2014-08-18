import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats, interpolate, signal
import random
from itertools import chain

import results

def choose_points(qr_list):
    return [d.total_response() - getattr(d, 'median', 0) for d in qr_list]


def check_data(data):
    """ graph the values """
#    data.median_filter(choose_points)
    for key, value in data.items():
        plt.plot([x.response[0] for x in value],
                 choose_points(value),
                 '.',
                 alpha=0.5,
                 label=str(key),
             )
    plt.plot([x.response[0] for x in data.all_as_timeseries()],
             [x.median for x in data.median_filter(choose_points)])
    plt.legend()
    plt.show()

data = results.read_data(bucket=r'^/api/\w{5}(\w)\w{4}/config$',
                         data_dir='more_recent_data')


check_data(data)
