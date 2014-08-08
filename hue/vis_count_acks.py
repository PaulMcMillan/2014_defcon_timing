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


def check_data(data):
    """ graph the values """
    tsdata = data.all_as_timeseries()
    res = defaultdict(int)
    for x in tsdata:
        res[x.response_count()] += 1
    pprint(res)

data = results.read_data(bucket=r'^/api/\w{5}(\w)\w{4}/config$',
                         filename='data/out.parsed')


check_data(data)
