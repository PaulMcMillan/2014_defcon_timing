import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats
import random
from itertools import chain

import results

def choose_points(data):
    return [d.content_break() for d in data]

def check_data(data):
    """compares a single sample against all other samples. Doesn't work
    very well.

    """
    data_roundup = defaultdict(int)
    for key in data.keys():
        data_copy = data.copy()
        del data_copy[key]
        copy_val = list(chain(*data_copy.values()))
        d, p = stats.ks_2samp(choose_points(data[key]), choose_points(copy_val))
        if p < 10.1:
            data_roundup[key] = p
            print 'Key: %s D: %s p:%s' % (key, d, p)
    return data_roundup


data = results.read_data(bucket=r'^/api/\w{5}(\w)\w{4}/config$',
                         filename='data/out.parsed')

pprint(dict(check_data(data)))
