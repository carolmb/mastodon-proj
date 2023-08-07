import json
import requests
import datetime
import pandas as pd

from bs4 import BeautifulSoup
from util import get_instance_token
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# data = pd.read_csv('toots_kuni_list.tsv', sep='\t')
# data = data.dropna(subset='in_reply_to_account_id')
# data = data.astype({'id':'int64', 'in_reply_to_account_id':'int64'})

def get_mentions():
    mentions = []
    for idx, row in data.iterrows():
        toot_id = row['id']
        toot_uri = row['uri']
        toot_content = row['content']
        toot_author = row['mastodon_name']
        if type(toot_content) == str:
            soup = BeautifulSoup(toot_content, 'html.parser')
            mentions_list = soup.find_all("a", {"class": "u-url mention"})
        else:
            mentions_list = [{'href':toot_author}]

        for item in mentions_list:
            mentioned = item['href']
            mentions.append(tuple((toot_author, mentioned, toot_id, toot_uri, toot_content)))

    mentions = pd.DataFrame(mentions, columns=['toot_author', 'mentioned_user', 'toot_id', 'uri', 'content'])

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_userid(user_instance, user_server):
    try:
        token_access = get_instance_token(user_server)
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

    
def mentioned_users():
    mentioned_id = []
    rename = []
    for idx, row in mentions.iterrows():
        try:
            #
            if row['mentioned_user'].startswith("https"):
                instance_user = row['mentioned_user'][8:].split('/@')
            else:
                instance_user = row['mentioned_user'].split("@")

            instance = instance_user[0]
            user = instance_user[1] 
    #         user_id = get_userid(user, instance)
            name = "{}@{}".format(user, instance)
        except:
            user_id = None
            name = None
            print(row)
    #     mentioned_id.append(user_id)
        rename.append(name)

    mentions['mentioned_user_instance'] = rename
    print(len(mentions))
    mentions = mentions.dropna(subset='mentioned_user_instance')


    count = 0
    mentioned_id = []
    for idx, row in mentions.iterrows():
        print(count, end='\r')
        count += 1
        instance = instance_user[0]
        user = instance_user[1] 
        user_id = get_userid(user, instance)
        mentioned_id.append(user_id)
    mentions['mentioned_id'] = mentioned_id

    mentions.to_csv('kuni_users_mentions.tsv', sep='\t')
    

def get_user_profile(server, user_instance):
    token_access = get_instance_token(server)
    url = 'https://{}/api/v1/accounts/lookup?acct={}'.format(server, user_instance)
    headers = {
        'Authorization' : 'Bearer {}'.format(token_access)
    }
    r = session.get(url, headers=headers)
    return r.json()
    

def mentioned_profile_info():
    data = pd.read_csv('kuni_users_mentions.tsv', sep='\t')
    print(data.head())
    data = data.dropna(subset='mentioned_id')
    print(len(data))
    profiles = []
    for idx, row in data.iterrows():
        print(idx, end='\r')
        mentioned_instance = row['mentioned_user_instance'].split('@')[-1]
        try:
            profile = get_user_profile(mentioned_instance,row['mentioned_user_instance'])
            profiles.append(profile)
        except:
            print("something went wrong", row['mentioned_user_instance'])

    today = datetime.datetime.now()
    pd.DataFrame(profiles).to_csv('mentioned_profiles_kuni_{}.tsv'.format(today), sep='\t')
    
data = pd.read_csv('mentioned_profiles_kuni_2023-08-07 01:20:19.437081.tsv', sep='\t')
print(len(data))
print(data.columns)
print(data['url'].head(100))