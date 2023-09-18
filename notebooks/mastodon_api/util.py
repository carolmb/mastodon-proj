import os
import sys
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


def get_save_instance_token(filename, instance):
    print('filename exists')
    file = open(filename).read().split('\n')
    client_id = file[0]
    client_secret = file[1]

    url = 'https://{}/oauth/token'.format(instance)
    params = {
        'client_id' : client_id,
        'client_secret' : client_secret,
        'redirect_uri' : 'urn:ietf:wg:oauth:2.0:oob',
        'grant_type' : 'client_credentials'
    }

    r = requests.post(url=url, params=params)
#     print('request code', r.status_code)
    token = open('../temp/token_{}.secret'.format(instance), 'w')
    token.write(r.text)
    token.close()

    token_json = json.loads(r.text)
    return token_json['access_token']


def get_instance_token(instance):
    filename = "../temp/mastodon_app_key_{}.secret".format(instance)
    
    if os.path.exists('../temp/token_{}.secret'.format(instance)):
        token_json = json.loads(open('../temp/token_{}.secret'.format(instance)).read())
#         print('token_json', token_json)
        return token_json['access_token']

    if os.path.exists(filename):
        return get_save_instance_token(filename, instance)
    else:
        try:
            Mastodon.create_app(
                'pytooterapp',
                api_base_url = 'https://{}'.format(instance),
                to_file = '../temp/mastodon_app_key_{}.secret'.format(instance)
            )
            return get_save_instance_token(filename, instance)
        except:
            print('error instance', instance)
            return None
    
