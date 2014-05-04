import time
import curl
import itertools
from scipy import stats
import random
import numpy as np

COUNT = 81250
SAMPLE_COUNT = 40000

def get_data(url='http://10.4.0.215'):
    print url
    c = curl.Curl(url)
    results = []
    while True:
        c.get()
        i = c.info()
        yield (i['starttransfer-time'] - i['pretransfer-time']) * 1000

def sfilter(ary1, ary2):
    std = np.std(ary1 + ary2)
    mean = np.mean(ary1 + ary2)
    return (filter(lambda x: x < mean + std, ary1),
            filter(lambda x: x < mean + std, ary2))

def readfile(name):
    res = []
    with open(name) as f:
        for x in f:
            res.append(float(x.strip()))
    return res

start = time.time()


#res = readfile('outsame1') + readfile('outsame2')
#res, res2 = readfile('outdiff1'), readfile('outdiff2')
res, res2 = readfile('outsame1'), readfile('outsame2')

res, res2 = sfilter(res, res2)

res = random.sample(res, SAMPLE_COUNT)
res2 = random.sample(res2, SAMPLE_COUNT)

print "Count: %s" % COUNT
print "KS D:%s p-value:%s" % stats.ks_2samp(res, res2)
print "Elapsed: %s" % (time.time() - start)
print stats.describe(res)

import matplotlib.pyplot as plt
plt.plot(res)
plt.plot(res2)
#plt.hist(res, bins=200, histtype='step')
#plt.hist(res2, bins=200, histtype='step')
plt.show()
