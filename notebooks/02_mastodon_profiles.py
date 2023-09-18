import os
import glob
import parse
import numpy as np
import pandas as pd
import datetime

from mastodon import Mastodon

mastodon_app = "acmbrito_app_python_secret"
client_id, client_secret, access_token, api_base_url = open(mastodon_app).read().split()
api1 = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    access_token=access_token,
    api_base_url=api_base_url
)

def get_userid(user_name, user_server):
    try:
        user_profile = api1.account_lookup("{}@{}".format(user_name, user_server))
        return user_profile["id"]
    except Exception as error:
        print(error)
        return None


def get_userprofile(user_server, field_name):
    user_profile = api1.account_lookup(user_server)

    tt_user = ""
    for field in user_profile["fields"]:
        if field["name"] == "Twitter":
            tt_user = field["value"]

    bio = user_profile["note"]
    created = user_profile["created_at"]
    display_name = user_profile["display_name"]
    followers = user_profile["followers_count"]
    following = user_profile["following_count"]

    return (
        user_server,
        display_name,
        tt_user,
        followers,
        following,
        created,
        bio.replace("\t", " "),
        field_name
    )


handle = ["mastodon", "account"]

def get_scholars_handles(files, str_format):
    mastodon_users = []
    for file in files:
        print(file)
        df = pd.read_csv(file, on_bad_lines="warn")
        for col in df.columns:
            if handle[0] in col.lower() or handle[1] in col.lower():
                scholars = df[col].dropna().values
                for row in scholars:
                    if row.startswith('@'):
                        row = row[1:]
                    try:
                        mastodon_users.append(get_userprofile(row,file))
                    except:
                        print('can\'t find', row)
                break
        

    return mastodon_users

files1 = glob.glob('csv/*.csv')
files2 = glob.glob('csv/others/*.csv')
# print(files2)
# mastodon_users = get_scholars_handles(files1, "csv/scholars_{}.csv")
# mastodon_users += get_scholars_handles(files2, "csv/others/{}.csv")
# output = pd.DataFrame(mastodon_users)
# output.to_csv('mastodon_profiles_github.tsv', sep='\t')


def get_scholars_fields(files, str_format):
    mastodon_users = []
    pair = []
    for file in files:
        print(file)
        df = pd.read_csv(file, on_bad_lines="warn")
        for col in df.columns:
            if handle[0] in col.lower() or handle[1] in col.lower():
                scholars = df[col].dropna().values
                for row in scholars:
                    if row.startswith('@'):
                        row = row[1:]
                    pair.append((row, file))
                break
    return pair
    
mastodon_users = get_scholars_fields(files1, "csv/scholars_{}.csv")
mastodon_users += get_scholars_fields(files2, "csv/others/{}.csv")
output = pd.DataFrame(mastodon_users)
output.to_csv('mastodon_profiles_fields.tsv', sep='\t')