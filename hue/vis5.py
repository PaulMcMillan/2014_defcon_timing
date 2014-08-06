import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats
import random
from itertools import chain


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
with open('data/16_s_0_4.parsed') as f:
    for line in f:
        qr = QueryResponse(*line.strip().split(','))
        if qr.path.startswith('/api/'):
                data[qr.path.replace('/api/', '')[5]].append(
                    qr)

common_params = dict(
#     bins=50,
# #     range=(0, 0.00035),
#      histtype='step',
#    style="ro",
      alpha=0.5,
    #normed=True,
     )

for key, value in data.items()[:1]:
#    value = value[:10000]
    for rlen in range(10):
        value2 = [x for x in value if x.response_count() == rlen]
        if len(value2):
            plt.plot([x.response[0] for x in value2],
                     [x.total() for x in value2],
                     '.',
                     label=str(key) + str(rlen), **common_params)
plt.legend()
try:
    plt.show()
except KeyboardInterrupt:
    plt.close()

