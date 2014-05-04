import time
import curl
import itertools
from scipy import stats

COUNT = 100#81250

def get_data(url='http://10.4.0.215'):
    print url
    c = curl.Curl(url)
    results = []
    while True:
        c.perform()
        i = c.info()
        yield (i['starttransfer-time'] - i['pretransfer-time']) * 1000

start = time.time()
resit  = get_data('http://169.254.159.24/api/newXevelopeX/lights/')
resit2 = get_data('http://169.254.159.24/api/newdevelopeX/lights/')

res = []
res2 = []
for x in range(COUNT):
    res.append(resit.next())
    time.sleep(0.05)
    res2.append(resit2.next())
    time.sleep(0.05)

with open('outdiff1', 'w') as f:
    for x in res:
        f.write('%s\n' % x)
with open('outdiff2', 'w') as f:
    for x in res2:
        f.write('%s\n' % x)

print "Count: %s" % COUNT
print "KS D:%s p-value:%s" % stats.ks_2samp(res, res2)
print "Elapsed: %s" % (time.time() - start)
print stats.describe(res)

print "\nSecond Phase...\n"

start = time.time()
resit  = get_data('http://10.4.0.215/api/newdevelopeX/lights/')
resit2 = get_data('http://10.4.0.215/api/newdevelopeX/lights/')

res = []
res2 = []
for x in range(COUNT):
    res.append(resit.next())
    time.sleep(0.05)
    res2.append(resit2.next())
    time.sleep(0.05)

with open('outsame1', 'w') as f:
    for x in res:
        f.write('%s\n' % x)
with open('outsame2', 'w') as f:
    for x in res2:
        f.write('%s\n' % x)

print "Count: %s" % COUNT
print "KS D:%s p-value:%s" % stats.ks_2samp(res, res2)
print "Elapsed: %s" % (time.time() - start)
print stats.describe(res)

# import matplotlib.pyplot as plt
# #plt.plot(res)
# #plt.plot(res2)
# plt.hist(res, bins=100, histtype='step')
# plt.hist(res2, bins=100, histtype='step')
# plt.show()
