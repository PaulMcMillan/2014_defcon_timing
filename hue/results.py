from collections import defaultdict
import re
import random
from itertools import chain
from scipy import signal

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

    def content_break(self):
        """ Experimental, seems mostly accurate on my setup """
        return self.response[5] - self.response[4]

    def _response_deltas(self):
        for x in range(len(self.response) - 1):
            yield self.response[x+1] - self.response[x]


class DataCollection(dict):
    def __missing__(self, arg):
        self[arg] = list()
        return self[arg]
    
    def minlen(self):
        return min(map(len, self.values()))
    
    def trim(self):
        minlen = self.minlen()
        for k, v in self.items():
            self[k] = v[:minlen]

    def sample(self, length, start=None):
        if start is None:
            start = random.randrange(self.minlen() - length)
        print length, start
        result = DataCollection()
        for k, v in self.items():
            result[k] = v[start:start+length]
        return result

    def all_as_timeseries(self):
        return sorted(chain(*self.values()), key=lambda x: x.response)

    def median_filter(self, point_function, kernel_size=55):
        all_ts = self.all_as_timeseries()
        filtered = signal.medfilt(point_function(all_ts),
                                  kernel_size=kernel_size)
        for qr, fv in zip(all_ts, filtered):
            qr.median = fv

def read_data(bucket=r'/api/(\w+)/config',
              filename='data/out.parsed',
              print_summary=True):

    data = DataCollection()
    with open(filename) as f:
        for line in f:
            qr = QueryResponse(*line.strip().split(','))
            match = re.match(bucket, qr.path)
            if match:
                data[match.group(1)].append(qr)

    if print_summary:
        for k, v in data.items():
            print k, len(v)

    return data