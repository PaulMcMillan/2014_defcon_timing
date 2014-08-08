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
#    data = data.sample(1501)
    data_roundup = defaultdict(int)
    for k1, k2 in combinations(data.keys(), 2):
        # DON'T EVER USE A SAMPLE SIZE THAT IS A MULTIPLE OF 100
        d, p = stats.ks_2samp(choose_points(data[k1]),
                              choose_points(data[k2]))
        print k1, k2, d, p
        if p < 0.1:
            data_roundup[k1] += 1
            data_roundup[k2] += 1

    return dict(data_roundup)

data = results.read_data(bucket=r'^/api/\w{3}(\w)\w{6}/config$',
                         filename='data/out.parsed')

#pprint(check_data(data))
#exit()
correct = 0
incorrect = 0
for x in range(30):
    res = check_data(data)
    pprint(res)
    if not res:
        continue
    if sorted(res.items(), key=lambda x: -x[1])[0][0] == '7':
        correct += 1
    else:
        incorrect += 1
print correct, incorrect, float(correct)/(incorrect + correct) * 100.0
        
