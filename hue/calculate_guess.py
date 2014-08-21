#!/usr/bin/env python
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats
import random
from itertools import chain
import sys

import users

import results


def choose_points(qr_list):
    return [d.total_response() for d in qr_list]


def analyze_data(data, p_threshold=0.05):
    """ combinatoric KS, add hits """
    data_roundup = defaultdict(int)
    for k1, k2 in combinations(data.keys(), 2):
        # DON'T EVER USE A SAMPLE SIZE THAT IS A MULTIPLE OF 100
        d, p = stats.ks_2samp(choose_points(data[k1]),
                              choose_points(data[k2]))
        print k1, k2, d, p
        if p < p_threshold:
            data_roundup[k1] += 1
            data_roundup[k2] += 1

    return dict(data_roundup)



def next_guess(data):
    # this is tuned for my device what a charset len of 8. Modify as
    # appropriate.
    res = analyze_data(data, p_threshold=0.1)
    pprint(res)
    values = sorted(res.values())
    if values and values[-1] >= 6:
        if (values[-1] - values[-2]) >= 2:
            if sum(values[:-1]) < 13: # ?
                return max(res, key=res.get)

if __name__=='__main__':
    prefix_len = 5
    data = results.read_data(bucket=r'^/api/(\w{%s})\w+/config$' % prefix_len,
                             data_dir='data',
                             postfix='.parsed')
    
    pprint(analyze_data(data, p_threshold=0.1))

# length = 1501
# incr_length = 101
# max_len = data.minlen()
# start = random.randint(0, max_len - length)

# while True:
# #    print length, start
# #    this_data = data.sample(length, start)
#     this_data = data
#     if next_guess(this_data):
#         print "Exiting", length, start, 
#         print (this_data['0000'][-1].query - this_data['0000'][0].query
#            ) / 1.0e9 / 60
#         exit()
#     length += incr_length # this doesn't wrap quite properly.
