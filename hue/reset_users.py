import json

import requests
from pprint import pprint

import discover

hue_url = discover.find_hue()
username = "timinguser"

print hue_url + 'api'
res = requests.post(hue_url + 'api', headers={'Content-Type': 'text/plain'},
                    data=json.dumps(
                        {"devicetype": "timinguser"}
#                         "username": username,}
                    ))
print res.json()
for message in res.json():
    if message.get('error'):
        if message['error']['type'] == 101:
            raise Exception(message['error']['description'])
    if message.get('success'):
        username = message['success']['username']

res = requests.get(hue_url + 'api/{}/config'.format(username)).json()
for user in res['whitelist'].keys():
    if user != username:
        res = requests.delete(hue_url + 'api/{}/config/whitelist/{}'.format(
            username, user))
        print res.json()
res = requests.get(hue_url + 'api/{}/config'.format(username)).json()
pprint(res['whitelist'])
