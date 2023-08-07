import ast
import swifter
import datetime
import pandas as pd

works_filename = 'openalex_preprocess/works_core+basic+authorship+ids+funding+concepts+references+mesh.tsv'
works = pd.read_csv(works_filename, sep='\t', chunksize=100000, dtype=object)

test1 = pd.read_csv('mastodon_users_wOpenAlex2.csv')
authors = test1['OpenAlex_account']

authors_ids = []
for row in authors:
    authors_ids.append(int(row.split('A')[1]))
authors_ids = set(authors_ids)
today = datetime.datetime.now()
print(today)

max_len = 10000
trend = []
count = 0
for chunk in works:
    chunk['authorships:author:id'] = chunk['authorships:author:id'].swifter.apply(lambda row: ast.literal_eval(row))
    for idx, row in chunk[['id','authorships:author:id', 'publication_year', 'referenced_works']].iterrows():
#         authors_list = ast.literal_eval(row['authorships:author:id'])
        for author in row['authorships:author:id']:
            if author in authors_ids:
                trend.append(row)
                count += 1
                print(count, end='\r')
    
                if len(trend) > max_len:
                    trend = pd.DataFrame(trend)
                    today = datetime.datetime.now()
                    trend.to_csv('temp/mastodon_users_papers_{}.tsv'.format(today), sep='\t')
                    trend = []
                    print('new file created')
    
if len(trend) > 0:
    today = timedate.timedate.now()                
    trend = pd.DataFrame(trend)
    trend.to_csv('temp/mastodon_users_papers_{}.tsv'.format(today), sep='\t')