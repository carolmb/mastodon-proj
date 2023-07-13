import os
import json
import requests

def get_instance_token(instance):
    filename = "temp/mastodon_app_key_{}.secret".format(instance)
    
    if os.path.exists('temp/token_{}.secret'.format(instance)):
        token_json = json.loads(open('temp/token_{}.secret'.format(instance)).read())
        return token_json['access_token']

    if os.path.exists(filename):
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
        print(r.status_code)
        token = open('temp/token_{}.secret'.format(instance), 'w')
        token.write(r.text)
        token.close()

        token_json = json.loads(r.text)
        return token_json['access_token']
    else:
        return False
    

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_user_lookup(user_name, user_server, token_access):
    try:
        url = 'https://{}/api/v1/accounts/lookup/'.format(user_server)
        headers = {
            'Authorization' : 'Bearer {}'.format(token_access)
        }
        params = {
            'acct' : '{}@{}'.format(user_name, user_server)
        }
        r = session.get(url, headers=headers, params=params)

        user = json.loads(r.text)
        return user
    except Exception as error:
        print(error)
        return None