import json
import datetime
import numpy as np
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
## toots in a instance
instance_name = 'sciencemastodon.com'
instance_token = '637b29fdad72ace2dcf18831'

url = 'https://{}/api/v1/timelines/public'.format(instance_name)
r = session.get(url, headers={'Authorization': "Bearer {}".format(instance_token)})

c = 1

to_save = []
datetime_str = '%Y-%m-%dT%H:%M:%S'
limit_date = datetime.datetime(2022, 9, 1)
i = 0
while True:
    c += 1
    test = json.loads(r.text)
    if len(test) == 0:
        print('aqui1')
        break
        
    print(test)
    created_at = test[-1]['created_at'][:-5]
    created_at = datetime.datetime.strptime(created_at, datetime_str)
    
    to_save += test
    try:
        next_id = test[-1]['id']
    except:
        print('error')
        print(test)
        break
        
    if next_id == None:
        print("aqui")
        break
    
    if c > 500:
        print(created_at)
        toots_from_instance = pd.DataFrame(to_save)
        toots_from_instance.to_csv('toots_from_{}_{}.tsv'.format(instance_name,i), sep='\t')
        i += 1
        del toots_from_instance
        to_save = []
    
    if limit_date > created_at:
        print(limit_date)
        print(created_at)
        break
#     r = requests.get(url, headers={'Authorization': "Bearer {}".format(instance_token)}, params={'max_id': next_id})
    r = session.get(url, headers={'Authorization': "Bearer {}".format(instance_token)}, params={'max_id': next_id})
toots_from_instance = pd.DataFrame(to_save)
toots_from_instance.to_csv('toots_from_{}.tsv'.format(instance_name), sep='\t')