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
    #print stats.describe(choose_points(data['2']))
    min_len = min(map(len, data.values()))
    print stats.kruskal(*[choose_points(d[:min_len]) for d in data.values()])
    print stats.wilcoxon(choose_points(data['1']), choose_points(data['2']))

data = results.read_data(bucket=r'^/api/\w{5}(\w)\w{4}/config$',
                         filename='data/out.parsed')

check_data(data)
