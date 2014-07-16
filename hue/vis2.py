import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats


class QueryResponse(object):
    """Class to make it easier to work with parsed data. Works with
    everything natively in nanoseconds.
    """
    # This offset is a convenience that makes it easier to avoid
    # losing precision if we start using floats. Pick the right value
    # for you.
    OFFSET = 1405000000000000000

    def __init__(self, *args):
        if len(args) < 3:
            print args
        self.host = args[0]
        self.path = args[1]
        self.query = self._parse(args[2])
        self.response = map(self._parse, args[3:])

    def _parse(self, nano_time):
        """ Parse a nansecond timestamp string into nanoseconds (integer) """
        # If we accidentally mix microsecond time, fix it to nano.
        seconds, nanoseconds = nano_time.split('.')
        return int('{}{:<9}'.format(seconds, nanoseconds)) - self.OFFSET

    def total(self):
        """ Time from Request to complete response. """
        return self.response[-1] - self.query

    def first_response(self):
        """ Time from request to first response. """
        return self.response[0] - self.query

    def total_response(self):
        """ Delta first response packet to last. """
        return self.response[-1] - self.response[0]

    def last_delta(self):
        """ Time from second to last packet, to last response packet. """
        return self.response[-1] - self.response[-2]

    def response_count(self):
        """ How many packets were in the response? """
        return len(self.response)

    def _response_deltas(self):
        for x in range(len(self.response) - 1):
            yield self.response[x+1] - self.response[x]


data = defaultdict(list)
with open('data/out.parsed') as f:
    for line in f:
        qr = QueryResponse(*line.strip().split(','))
        if qr.path.startswith('/api/'):
            data[qr.path.replace('/api/', '')[:24]].append(qr.total_response())
for k, v in data.items():
    print k, len(v)
data_roundup = defaultdict(int)
for s1, s2 in combinations(data.keys(), 2):
    d, p = stats.ks_2samp(data[s1][5000:16500],data[s2][5000:16500])
    if p < 0.05:
        data_roundup[s1] += 1
        data_roundup[s2] += 1
        print s1, s2,
        print ' D: %s p:%s' % (d, p)
pprint(dict(data_roundup))

# def parse_data():
#     results = defaultdict(list)
#     for x in data:
#         if len(x) <= 80:
#             category = len(x[1])
#             try:
#                 diff = float(x[-1]) - float(x[3])
#             except IndexError:
#                 print x
#             results[category].append(diff)
#     print results.keys()
#     return results

common_params = dict(
    # bins=3000,
    # range=(0, 0.00035),
    # histtype='step',
    # alpha=0.5,
    )

# for key, value in parse_data().items():
#     if key in [42, 43, 44]:
#         plt.plot(sorted(value[:1200]), label=str(key), **common_params)
# #plt.plot(sorted(parse_data('')), label='all', **common_params)
# plt.legend()
# plt.show()
