# coding: utf-8

# In[22]:


import numpy as np
import pandas as pd
from pandas import DataFrame
import MySQLdb
import os
from datetime import datetime
import csv

from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from fuzzywuzzy import fuzz

finalresultttt = ''


##define functions
def fuzzy_matching(mapper, fav_movie, verbose=True):
    match_tuple = []
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_movie.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print('Oops! No match is found')
        return
    if verbose:
        print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
    return match_tuple[0][1]


def make_recommendation(model_knn, data, mapper, fav_movie, n_recommendations):
    # fit
    # print(data)
    model_knn.fit(data)
    print('You have input news:', fav_movie)
    idx = fuzzy_matching(mapper, fav_movie, verbose=True)
    print(idx)
    if (idx == None):
        print("No Recommendations")  ##Replace by content based model
    else:
        print('Recommendation system start to make inference')
        print('......\n')
        distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations + 1)
        raw_recommends = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                key=lambda x: x[1])[:0:-1]
        reverse_mapper = {v: k for k, v in mapper.items()}
        print('Recommendations for {}:'.format(fav_movie))
        resultss = ''
        with open('my_csv.csv', 'a') as f:
            for i, (idx, dist) in enumerate(raw_recommends):
                recResults = df.loc[df['Title'] == reverse_mapper[idx]]
                rresults = recResults['Dictionary']
                rresults.to_csv(f, index=False)
        with open('my_csv.csv') as file:
            reads = csv.reader(file)
            for row in reads:
                ffinalresult = row[0] + ","
                resultss = resultss + ffinalresult

        finalresultttt = resultss[:-1]
        print(finalresultttt)  ##FinalResult for Colloborative filtering
        os.remove('my_csv.csv')


##Read user info from the db for the user
userId = '10';  ##get logged in user id
conn = MySQLdb.connect(host='localhost', user='root', passwd='root')
cursor = conn.cursor()
cursor.execute('use rsystem')
cursor.execute('select first_login from users where id=' + userId)
result = cursor.fetchone()[0]
df = pd.read_csv(
    "C:\\Users\\Taman\\Downloads\\drive-download-20190512T040150Z-001\\Scrape_Data_Times_10.csv")  ##Change the path
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)

##FirstUserLogin then Content Based Model
if (result == 'Y'):
    print(result)
    cursor.execute('select preferences from preferences where user_id=' + userId)
    result = cursor.fetchone()[0]
    print(result)
    noOfPreferences = result.split(",")
    print("Number of Preferences:" + str(len(noOfPreferences)))

    if (len(noOfPreferences) > 1):
        for y in noOfPreferences:
            with open('dictionarycsv.csv', 'a') as f:
                dictionary = df.loc[df['Section'] == y]
                writetocsv = dictionary['Dictionary'].head(3)
                # print(writetocsv)
                writetocsv.to_csv(f, index=False)
    else:
        dictionary = df.loc[df['Section'] == noOfPreferences[0]]
        writetocsv = dictionary['Dictionary'].head(3)
        # print(f)
        writetocsv.to_csv("dictionarycsv.csv", index=False)

    results = ''
    ##JSON FORMAT
    with open('dictionarycsv.csv') as infile:
        read = csv.reader(infile)
        for row in read:
            finalresult = row[0] + ","
            t = open("json.txt", "a+")
            t.write(finalresult)
            t.close()
            results = results + finalresult

    finalresultttt = results[:-1]
    articles = "["+finalresultttt+"]"
    print(articles)  ##FinalResult for Content Based
    os.remove('dictionarycsv.csv')

else:
    ##Collaborative Item based knn filtering
    ##Change the path
    df_matrix = pd.read_csv(
        "C:\\Users\\Taman\\Downloads\\drive-download-20190512T040150Z-001\\Scrape_Data_Lite_Times_10.csv")
    news_user_mat = df.pivot(index='ID', columns='Topic', values='Rating').fillna(0)
    news_to_idx = {
        news: i for i, news in
        enumerate(list(df_matrix.set_index('ID').loc[news_user_mat.index].Title))
    }
    news_user_mat_sparse = csr_matrix(news_user_mat.values)
    model_knn = NearestNeighbors(metric='euclidean', algorithm='auto', n_neighbors=10, n_jobs=-1)
    model_knn.fit(news_user_mat_sparse)
    cursor.execute('use rsystem')
    cursor.execute('select news_title from user_history where user_ID=' + userId + ' order by id desc')
    result = cursor.fetchone()
    print(result)
    if (result == None):
        print("in none")
        my_favorite = 'Drug prices must be revealed in TV ads under new Trump rule'
    else:
        print("in else")
        my_favorite = result[0]

    make_recommendation(model_knn=model_knn, data=news_user_mat_sparse, fav_movie=my_favorite, mapper=news_to_idx,
                        n_recommendations=5)



