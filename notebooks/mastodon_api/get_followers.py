import os
import sys
import util
import json
import glob
import parse
import requests
import datetime

import numpy as np
import pandas as pd

from mastodon import Mastodon
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def user_followers(instance, user_id, access_token):
    URL = 'https://{}/api/v1/accounts/{}/followers'.format(instance, user_id)
    followers = []
    params = {}
    if access_token:
        headers = {
            'Authorization' : 'Bearer {}'.format(access_token)
        }

        #time.sleep(1)
        while True:
            r = session.get(URL, headers=headers, timeout=60)
            if r.text == None:
                break
            try:
                toots = json.loads(r.text)
            except:
                print('error', r.text)
                break
    #             print(toots)
            if 'link' in r.headers:
                URL = r.headers['link'].split(';')[0][1:-1]
                followers += toots
                if 'since_id=' in URL:
                    break
                if len(toots) == 0:
                    break
                if 'error' in toots:
                    print(user_id, toots)
                    break
            else:
                break
    return followers


user_id_map = pd.read_csv('../user111_id_list_kunilist_2023-06-30.tsv', sep='\t')
user_id_map = user_id_map.drop_duplicates(subset=['user', 'instance'])
user_id_map = user_id_map.dropna()

print('total of users', len(user_id_map))

user_id_map['mastodon_name'] = user_id_map.apply(lambda row: "{}@{}".format(row['user'], row['instance']), axis = 1)
user_id_map.head()

saved_users_files = glob.glob('kuni_scholars_followers_*.json')
saved_users = set()
for file in saved_users_files:
    current_saved = json.loads(open(file).read())
    print(len(current_saved))
    saved_users |= set(current_saved.keys())

print('total of saved users', len(saved_users))

output = dict()
max_users = 1000
for idx, user in user_id_map.iterrows():
    if user['mastodon_name'] in saved_users:
        continue
    print(user['mastodon_name'])
    
    instance_token = util.get_instance_token(user['instance'])
    if instance_token:
        followers = user_followers(user['instance'], user['user_id'], instance_token)
        output[user['mastodon_name']] = followers
        if len(output) > max_users:
            now = datetime.datetime.now()
            open('kuni_scholars_followers_{}.json'.format(now), 'w').write(json.dumps(output))
            print('aqui')
            output = dict()
        print()

now = datetime.datetime.now()
open('kuni_scholars_followers_{}.json'.format(now), 'w').write(json.dumps(output))
