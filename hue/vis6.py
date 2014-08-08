import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats
import random
from itertools import chain

import results

def choose_points(data):
    return [d.total_response() for d in data]


def check_data(data):
    """ combinatoric KS, add hits """
#    data = data.sample(10000)
    data_roundup = defaultdict(int)
    for k1, k2 in combinations(data.keys(), 2):
        d, p = stats.ks_2samp(choose_points(data[k1]),
                              choose_points(data[k2]))
        print k1, k2, d, p
        if p < 0.05:
            data_roundup[k1] += 1
            data_roundup[k2] += 1

    return dict(data_roundup)

data = results.read_data(bucket=r'^/api/\w{3}(\w)\w{6}/config$',
                         filename='data/out.parsed')


pprint(check_data(data))
