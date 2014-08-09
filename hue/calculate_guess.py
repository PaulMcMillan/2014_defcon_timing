#!/usr/bin/env python
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats
import random
from itertools import chain

import results


def choose_points(qr_list):
    return [d.total_response() for d in qr_list]


def check_data(data, p_threshold=0.1):
    """ combinatoric KS, add hits """
    data = data.sample(3501)
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

data = results.read_data(bucket=r'^/api/\w{3}(\w)\w{6}/config$',
                         filename='data/out.parsed')

#pprint(check_data(data))
#exit()
correct = 0
incorrect = 0
unclear = 0
shortened = []
shorten_error = 0
ANSWER = '0'
for x in range(1000):
    print "Iteration: ", x
    res = check_data(data)
    if not res:
        unclear += 1
        continue
    if ANSWER not in res.keys() and max(res.values()) >= 4:
        pprint(res)
        print "shorten error"
        shorten_error += 1
    if max(res.values()) >= 4 and len(res.values()) < 8:
        shortened.append(8 - len(res.values()))
    sri =  sorted(res.items(), key=lambda x: -x[1])
    pprint(sri)
    if sri[0][0] == ANSWER and sri[0][1] <= sri[1][1] + 2 and sri[0][1] <= 5:
        unclear += 1
    elif sri[0][0] == ANSWER:
        correct += 1
    else:
        incorrect += 1
print correct, incorrect, float(correct)/(incorrect + correct) * 100.0
print "shorten error ", shorten_error, " unclear: ", unclear
print "Shortened: ", len(shortened), shortened

