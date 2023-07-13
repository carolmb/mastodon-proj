# -*- coding: utf-8 -*-
"""Mstdn_keywords.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X6JCWFHgiIDo-faommQcTji3ZIEc_oh7
"""

!pip install Mastodon.py

import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt 
import networkx as nx

import mastodon 
from mastodon import Mastodon

m= Mastodon(access_token = 	'eTunZVjjC8_2N3bkcF0OMOYgPfqEOHzdg3UJ7msQjnA',
    api_base_url = 'https://mastodon.social')

prof_list = m.search(['professor', 'phd', 'PhD'], result_type= 'accounts')

print(len(prof_list))

prof_list_acc= prof_list.get('accounts')

print(len(prof_list_acc))

df = pd.DataFrame()

prof_ids = [] 
prof_username = [] 
prof_bio = [] 
for prof in prof_list_acc: 
  prof_ids.append((prof.get('id')))
  prof_username.append(prof.get('username'))
  #prof_bio(prof.get('note'))

print(len(prof_ids))

for prof in prof_list_acc: 
  prof_bio.append(str(prof.get('note')))

print(len(prof_bio))

df['ids'] = prof_ids
df['username'] = prof_username
df['bio'] = prof_bio

df.head()

def retrieve_acc_with_keyword(keyword): 
  results = m.search(q= keyword, result_type='accounts')
  print(results)
  df = pd.DataFrame()
  ids = [] 
  username = [] 
  bio = [] 
  final_results = results.get('accounts')
  for result in final_results: 
    ids.append(result.get('id'))
    username.append(result.get('username'))
    bio.append(str(result.get('note')))
  
  df['ids'] = ids
  df['username'] = username
  df['bio'] = bio 
  return df

retrieve_acc_with_keyword('phd')

