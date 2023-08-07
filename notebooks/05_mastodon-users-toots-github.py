#!/usr/bin/env python
# coding: utf-8

import time
import glob
import util
import json
import os.path
import requests
import pandas as pd
from datetime import datetime
from  datetime import date

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def get_userid(user_instance, user_server, token_access):
    try:
        url = 'https://{}/api/v1/accounts/lookup/'.format(user_server)
        headers = {
            'Authorization' : 'Bearer {}'.format(token_access)
        }
        params = {
            'acct' : user_instance
        }
        r = session.get(url, headers=headers, params=params)

        user = json.loads(r.text)
        if 'id' in user:
            return user["id"]
        elif 'user' in user:
            return user["user"]
    except Exception as error:
        print(error)
        return None

def get_instance_token(instance):
    return util.get_instance_token(instance)


def user_toots(instance, user_id, access_token):
    URL = 'https://{}/api/v1/accounts/{}/statuses'.format(instance, user_id)
    user_toots = []
    if access_token:
        headers = {
            'Authorization' : 'Bearer {}'.format(access_token)
        }
        
        user_toots = []
        params = {}
        while True:
            #time.sleep(1)
            r = requests.get(URL, headers=headers, params=params, timeout=60)
            toots = json.loads(r.text)
            user_toots += toots
            if len(toots) == 0:
                break
            if 'error' in toots:
                print(user_id, toots)
                break
            max_id = toots[-1]['id']
            params = {'max_id' : max_id}
            
            date_str = toots[-1]['created_at'].split('T')[0]
            last_date = date.fromisoformat(date_str)
            if last_date < date_limit:
                break

    return user_toots


date_limit = date(2022, 9, 1)

users = pd.read_csv('mastodon_profiles_github.tsv', sep='\t', encoding_errors='replace', on_bad_lines='warn')
users.columns = ['index', 'user_instance', 'display_name', 'twitter', 'followers', 'following', 'created_at', 'bio', 'field']


valid_fields = ['id',
'created_at',
'in_reply_to_account_id',
'uri',
'replies_count',
'reblogs_count',
'favourites_count',
'content'
]

'''
ids = []
i = 0
for _, user in users.iterrows():
    instance = user['user_instance'].split('@')[-1]
    instance_token = get_instance_token(instance)
    user_id = get_userid(user['user_instance'], instance, instance_token)
    ids.append((user['user_instance'], user_id))
    i += 1
    if i % 500 == 0:
        print(i, end='\r')
        pd.DataFrame(ids, columns=['user_instance', 'user_id']).to_csv('user_github_id_list.tsv', sep='\t')
pd.DataFrame(ids, columns=['user_instance', 'user_id']).to_csv('user_github_id_list.tsv', sep='\t')
'''

files = glob.glob('temp/users_toots_github_2023-07-* *.tsv')
print(files)
users_already_collected = []
invalid_users = set()
for file in files:
    invalid_users |= set(pd.read_csv(file, sep='\t')['user_id'])

print(len(invalid_users))


today = datetime.now()
outputs = []
size = 0
user_id_map = pd.read_csv('user_github_id_list.tsv', sep='\t')
user_id_map = user_id_map.drop_duplicates(subset=['user_instance', 'user_id'])
user_id_map = user_id_map.dropna()

for _, user in users.iterrows():
    user_id = user_id_map[user_id_map['user_instance'] == user['user_instance']]
    
    if len(user_id) >= 1:
        user_id = user_id['user_id'].values[0]
    else:
        continue

    if not user_id:
        print(user)
        continue

    if not user_id.isnumeric():
        continue

    if int(user_id) in invalid_users:
        print('aqui')
        continue
        
        
    instance_name = user['user_instance'].split('@')[-1]
    instance_token = get_instance_token(instance_name)
    if not instance_token:
        continue

    toots = user_toots(instance_name, user_id, instance_token)
    if len(toots) > 0:
        if 'error' not in toots:
            print(toots[:3])
            toots_pd = pd.json_normalize(toots)
            toots_pd = toots_pd.loc[:, valid_fields]
            toots_pd['user_id'] = user_id
            size += len(toots_pd)
            outputs.append(toots_pd)

    if size > 10000:
        data_toots = pd.concat(outputs)
        today = datetime.now()
        data_toots.to_csv('temp/users_toots_github_{}.tsv'.format(today), sep='\t')
        outputs = []
        size = 0

today = datetime.now()
data_toots = pd.concat(outputs)
data_toots.to_csv('temp/users_toots_github_{}.tsv'.format(today), sep='\t')
