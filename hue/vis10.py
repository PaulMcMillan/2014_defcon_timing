import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from pprint import pprint
from scipy import stats, signal
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
with open('data/out.parsed') as f:
    for line in f:
        qr = QueryResponse(*line.strip().split(','))
        if qr.path.startswith('/api/'):
#            if qr.response_count() > 7:
                data[qr.path.replace('/api/', '')[5]].append(
                    qr)

common_params = dict(
#     bins=1000,
#     range=(2.86 * 10**7, 2.87 * 10**7),
#      histtype='step',
#    style="ro",
      alpha=0.5,
    #normed=True,
     )
plt.plot(signal.medfilt([x.total() for x in data['3']], kernel_size=3))
plt.show()
exit()
for key, value in data.items()[:]:
#    value = value[:10000]
    # for rlen in range(10):
    #     value2 = [x for x in value if x.response_count() == rlen]
    #     if len(value2):
            value2 =  value
            print signal.medfilt([[x.response[5] - x.response[4] for x in value2]], kernel_size=3),
            plt.plot(#[x.response[0] for x in value2],
                     
                     '.',
                     label=str(key) , **common_params)
plt.legend()
try:
    plt.show()
except KeyboardInterrupt:
    plt.close()

