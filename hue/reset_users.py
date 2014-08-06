import json
import random
from pprint import pprint

import requests

import users
import discover

hue_url = discover.find_hue()

request_dict = {
    "devicetype": "timinguser",
    "username": users.generate_username(),
    }
res = requests.post(hue_url + 'api', headers={'Content-Type': 'text/plain'},
                    data=json.dumps(request_dict))
print res.json()
for message in res.json():
    if message.get('error'):
        raise Exception(message['error']['description'])
    if message.get('success'):
        username = message['success']['username']
        with open('username', 'w') as f:
            f.write(username)

res = requests.get(hue_url + 'api/{}/config'.format(username)).json()
for user in res['whitelist'].keys():
    if user != username:
        res = requests.delete(hue_url + 'api/{}/config/whitelist/{}'.format(
            username, user))
        print res.json()

res = requests.get(hue_url + 'api/{}/config'.format(username)).json()
pprint(res['whitelist'])
