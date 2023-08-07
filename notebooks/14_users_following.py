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

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_instance_token(instance):
    return util.get_instance_token(instance)


fields = ['id', 'acct', 'locked', 'bot', 'discoverable', 'created_at', 'note', 'followers_count', 'following_count', 'statuses_count', 'last_status_at', 'fields']

def user_following(user):
    user_instance = user['user_instance']
    instance_name = user_instance.split("@")[-1]
    user_id = user['user_id']
    instance_token = get_instance_token(instance_name)
    
    URL = 'https://{}/api/v1/accounts/{}/following'.format(instance_name, user_id)
    
    
    following = []
    if instance_token:
        headers = {
            'Authorization' : 'Bearer {}'.format(instance_token)
        }
        
        user_toots = []
        params = {}
        
        while True:
            #time.sleep(1)
            r = requests.get(URL, headers=headers, params=params, timeout=60)
            try:
                raw_following = r.json()
            except requests.exceptions.JSONDecodeError:
                print(r.text)
                if len(following) > 0:
                    return following
                else:
                    return []
            for profile in raw_following:
                row = [user_instance]
                for field in fields: 
                    if field in profile:
                        row.append(profile[field])
                following.append(tuple(row))
            
            if len(following) == 0:
                break
            if 'error' in following:
                print(user_id, following)
                break
            if 'Link' in r.headers:
                next_pg = r.headers['Link'].split('; rel')[0]
                URL = next_pg[1:-1]
                if 'since' in URL:
                    break
            else:
                break

    return following

files = glob.glob('temp/users_following_kuni_*.tsv')
print(files)
if len(files) > 0:
    invalid_users = []
    for file in files:
        invalid_users.append(pd.read_csv(file, sep='\t'))

    invalid_users = pd.concat(invalid_users)
    print(invalid_users.columns)
    invalid_users = set(invalid_users['0'])
else:
    invalid_users = set()

outputs = []
size = 0
user_id_map = pd.read_csv('user111_id_list_kunilist_2023-06-30.tsv', sep='\t')
user_id_map['user_instance'] = user_id_map.apply(lambda row: "{}@{}".format(row[1], row[2]), axis=1)
# user_id_map = user_id_map.drop_duplicates(subset=['user_instance', 'user_id'])
print(user_id_map.head())
user_id_map = user_id_map.dropna()


for _, user in user_id_map.iterrows():
    print(user)
    
    if user['user_instance'] in invalid_users:
        continue
    
    following = user_following(user)
    if len(following) > 0:
        outputs += following

    if len(outputs) > 10000:
        today = datetime.now()
        data_toots = pd.DataFrame(outputs)
        data_toots.to_csv('temp/users_following_kuni_{}.tsv'.format(today), sep='\t')
        outputs = []
        size = 0

        
if len(outputs) > 0:
    today = datetime.now()
    data_toots = pd.DataFrame(outputs)
    data_toots.to_csv('temp/users_following_kuni_{}.tsv'.format(today), sep='\t')
