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

def get_posts(user):
    URL = 'https://{}/api/v1/accounts/{}/statuses'.format(instance, user_id)
    posts = []
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
                posts += toots
                if 'since_id=' in URL:
                    break
                if len(toots) == 0:
                    break
                if 'error' in toots:
                    print(user_id, toots)
                    break
            else:
                break
    return posts

    
def get_mentions_of(user):
    pass


users = pd.read_csv('kuni_scholars_followers_merged_07-09_profiles.tsv', sep='\t')
print(len(users))
print(users.columns)
for idx, row in users[:10].iterrows():
    print(row['url'])
    # proximo passo é pegar user e server
    # então as postagens
    # filtrar as menções
