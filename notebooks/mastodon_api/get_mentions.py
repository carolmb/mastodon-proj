import os
import sys
import util
import json
import tqdm
import glob
import parse
import requests
import datetime

import numpy as np
import pandas as pd

from mastodon import Mastodon
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def get_posts_v2(instance, access_token, user_id):
#     URL = 'https://{}/api/v1/accounts/{}/statuses/?min_id=1'.format(instance, user_id)
    URL = 'https://{}/users/{}/outbox'.format(instance, user_id)
#     print(URL)
    toots = []
    params = {}
    if access_token:
        headers = {
            'Authorization' : 'Bearer {}'.format(access_token)
        }
        r = util.session.get(URL, headers=headers, timeout=60)
        r = r.json()
        if 'totalItems' in r:
            total_items = r['totalItems']
            first_url = r['last']
        else:
            print('can\'t access user', user_id, instance)
            return []
        
        while True:
            r = util.session.get(first_url, headers=headers, timeout=60)
            r = r.json()
            try:
                content = r['orderedItems']
                toots += content
                print(r.keys())
            except:
                print('error', r.keys())
                break
            if 'prev' in r:
                print('raw url', r['prev'])
                first_url = r['prev']

            else:
                return toots
#                 SOURCE HOW TO GET STATUSES https://www.reddit.com/r/Mastodon/comments/ynb0wm/how_would_i_get_only_a_single_users_statuses_with/
#                 https://docs.joinmastodon.org/api/guidelines/#pagination
    return toots

def get_posts(instance, access_token, user_id):
    url = 'https://{}/api/v1/accounts/{}/statuses?min_id=1'.format(instance, user_id)
    toots = []
    if access_token:
        headers = {
            'Authorization' : 'Bearer {}'.format(access_token)
        }
        while True:
            if url == None:
                break
                
            try:
                r = util.session.get(url, headers=headers, timeout=60)
                if r.status_code == 200:
                    content = r.json()
                    toots += content

                    url = None
                    if 'Link' in r.headers:
                        links = r.headers['Link'].split(', ')
                        for pag in links:
                            if 'prev' in pag:
                                url = pag.split("; ")[0]
                                url = url[1:-1] 
                else:
                    break
            except:
                print('error', url)
                break
            
                
    print(len(toots))
    return toots
        
    
def get_mentions_of(user):
    pass


already_saved = set()
files = glob.glob('posts_following/posts_all_users_following_scholars_*.json')
for file in files:
    data = pd.read_json(file)
    for row in data['account']:
        already_saved.add(row['username'].lower())

print('already saved', len(already_saved))

users = pd.read_csv('kuni_scholars_followers_merged_07-09_profiles.tsv', sep='\t')
users = users.drop_duplicates(subset='username')
print(users.head())
total = len(users)
print('total number of users', total)

posts_all_users = []
for idx, row in tqdm.tqdm(users.iterrows(), total=total):

    user_url = row['url']
    user_url = user_url[8:].split('/@')
    
    if len(user_url) <= 1:
        print('error', user_url)
        continue
        
    mastodon_name = user_url[1]
    if mastodon_name in already_saved:
        # print('already saved', mastodon_name)
        continue
    
    instance = user_url[0]
    access_token = util.get_instance_token(instance)
    
    if access_token == None:
        continue
    
    user_id = util.get_userid(mastodon_name, instance, access_token)
    posts = get_posts(instance, access_token, user_id)
    posts_all_users += posts
    
    if len(posts_all_users) > 10000:
        output_str = json.dumps(posts_all_users)
        time = datetime.datetime.now()
        output = open('posts_all_users_following_scholars_{}.json'.format(time), 'w')
        output.write(output_str)
        output.close()
        posts_all_users = []
#     posts = get_posts(instance, access_token, mastodon_name)

if len(posts_all_users) > 0:
    output_str = json.dumps(posts_all_users)
    time = datetime.datetime.now()
    output = open('posts_all_users_following_scholars_{}.json'.format(time), 'w')
    output.write(output_str)
    output.close()
    posts_all_users = []


# proximo passo é pegar user e server
# então as postagens
# filtrar as menções
