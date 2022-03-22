# def Articles():
#     articles =[
#         {
#             'id':"1",
#             'category':"Entertainment",
#             'title': "The Walking Dead's Final Episode Is A Satisfying Ending",
#             'description': 'The Walking Dead: The Final Season started strong, with Telltale&rsquo;s talented storytellers crafting a compelling new scenario for Clementine to navigate. After the company&rsquo;s closure, the fate of the season looked shaky, and Skybound Games took over finishing it up.  Ultimately, the finale sticks the landing, closing...',
#             'website': 'www.kotaku.com.au',
#             'images': 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/dbbx1dnhlfqhevormf6f.jpg'
#         },
#         {
#             'id': "2",
#             'category': "Technology",
#             'title': 'ShadowHammer Malware Attack: ASUS Responds',
#             'description': "It's the sort of thing you never want to happen. Researchers from Kaspersky Lab found that hackers had infiltrated ASUS, one of the biggest computer manufacturers in the world, and masked a backdoor &quot;ShadowHammer&quot; trojan as a legitimate update that was then pushed out to users through the ASUS Live Update tool.  ASUS...",
#             'website': 'www.kotaku.com.au',
#             'images': 'https://edge.alluremedia.com.au/m/g/2018/06/FDB9ADFF-3939-4C04-8563-A8BDBA4DD0BC-768x432.jpeg'
#         },
#         {
#             'id': "3",
#             'category': "Politics",
#             'title': "Anthem's New Update Adds More Loot, More Bugs",
#             'description': 'Stop me if you&rsquo;ve heard this one before. Anthem gets a new update. The changes in the new update all look promising. Then, upon closer inspection, not all of the improvements are working as intended, and a few things that had previously been fixed are now busted again....',
#             'website': 'www.kotaku.com.au',
#             'images': 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/ykwndrjcj5v8jxgegyes.jpg'
#         },
#         {
#             'id': "4",
#             'category': "Sports",
#             'title': 'RPG Publisher Says Chinese Government Burned Every Copy Of Their Latest Book',
#             'description': 'Sons of the Singularity, a small publisher of RPGs, ran a Kickstarter last year for a Call of Cthulu sourcebook, successfully raising over $28,097. Called The Sassoon Files, it was finally printed last week, only for the publisher to claim that the Chinese government then stepped in and burned every copy....',
#             'website': 'www.kotaku.com.au',
#             'images': 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/txpqjpnasegtvdokfwsz.jpg'
#         },
#         {
#             'id': "5",
#             'category': "Entertainment",
#             'title': 'The Dreams Of A Man Asleep For Three Weeks',
#             'description': 'On March 22, 2018, I was rushed to the hospital for life-saving surgery. Due to complications with the procedure, I didn&rsquo;t regain full, coherent consciousness until the second week in April. For three weeks I was stuck inside my own mind, subject to a seemingly unending series of dreams.  Dreams covering on a...',
#             'website': 'www.kotaku.com.au',
#             'images': 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/jcionlv3rdwedzfeddue.jpg'
#         },
#         {
#             'id': "6",
#             'category': "Science",
#             'title': 'Why you need to update your iPhone to iOS 12.2 immediately',
#             'description': 'If you use an iPhone, you should download iOS12.2 immediately or you will put yourself at risk.',
#             'website': 'www.9news.com.au',
#             'images': 'http://prod.static9.net.au/_/media/2018/08/03/11/31/iphone-x-fin-cut-sales.jpg'
#         },
#         {
#             'id': "7",
#             'category': "Entertainment",
#             'title': 'Sekiro Shadows Die Twice:&nbsp;The Kotaku&nbsp;Review',
#             'description': 'In Sekiro: Shadows Die Twice, the thread between life and death is tenuous. As the One-Armed Wolf, a loyal shinobi seeking to save a young noble with a cursed bloodline, you traverse a feudal Japan so saturated with the remnants of war that the idea of mortality becomes fickle: dead bodies blending in with the local...',
#             'website': 'www.kotaku.com.au',
#             'images': 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/binyqp1jtmvu5fku9jpo.jpg'
#         },
#         {
#             'id': "8",
#             'category': "Entertainment",
#             'title': 'EVE Online Player Is The First To Visit Every Star System In The Game',
#             'description': 'Exploring the entirety of space is impossible in the real world, but it&rsquo;s now been done in EVE Online. A player by the in-game name Katia Sae is the first player to have officially visited every one of the game&rsquo;s 7,805 star systems. Even more impressive, they did it without losing a single ship to EVE&rsquo;s...',
#             'website': 'www.kotaku.com.au',
#             'images': 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/l3zb2bzvh6jdxtno81bt.jpg'
#         }
#     ]
#     return articles


# coding: utf-8

# In[22]:
# import json
#
# import numpy as np
# import pandas as pd
# from pandas import DataFrame
# import MySQLdb
# import os
# from datetime import datetime
# import csv
#
# from sklearn.neighbors import NearestNeighbors
# from scipy.sparse import csr_matrix
# from fuzzywuzzy import fuzz
#
# finalresultttt = ''
#
#
# ##define functions
# def fuzzy_matching(mapper, fav_movie, verbose=True):
#     match_tuple = []
#     for title, idx in mapper.items():
#         ratio = fuzz.ratio(title.lower(), fav_movie.lower())
#         if ratio >= 60:
#             match_tuple.append((title, idx, ratio))
#     # sort
#     match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
#     if not match_tuple:
#         print('Oops! No match is found')
#         return
#     if verbose:
#         print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
#     return match_tuple[0][1]
#
#
# def make_recommendation(model_knn, data, mapper, fav_movie, n_recommendations):
#     # fit
#     # print(data)
#     model_knn.fit(data)
#     print('You have input news:', fav_movie)
#     idx = fuzzy_matching(mapper, fav_movie, verbose=True)
#     print(idx)
#     if (idx == None):
#         print("No Recommendations")  ##Replace by content based model
#     else:
#         print('Recommendation system start to make inference')
#         print('......\n')
#         distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations + 1)
#         raw_recommends = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
#                                 key=lambda x: x[1])[:0:-1]
#         reverse_mapper = {v: k for k, v in mapper.items()}
#         print('Recommendations for {}:'.format(fav_movie))
#         resultss = ''
#         with open('my_csv.csv', 'a') as f:
#             for i, (idx, dist) in enumerate(raw_recommends):
#                 recResults = df.loc[df['Title'] == reverse_mapper[idx]]
#                 rresults = recResults['Dictionary']
#                 rresults.to_csv(f, index=False)
#         with open('my_csv.csv') as file:
#             reads = csv.reader(file)
#             for row in reads:
#                 try:
#                     ffinalresult = row[0] + ","
#                 except:
#                     pass
#                 resultss = resultss + ffinalresult
#
#         finalresultttt = resultss[:-1]
#         print(finalresultttt)  ##FinalResult for Colloborative filtering
#         os.remove('my_csv.csv')
#
#
# ##Read user info from the db for the user
# userId = '35';  ##get logged in user id
# conn = MySQLdb.connect(host='localhost', user='root', passwd='')
# cursor = conn.cursor()
# cursor.execute('use myflaskapp')
# cursor.execute('select first_login from users where id=' + userId)
# result = cursor.fetchone()[0]
# my_path = os.path.abspath(os.path.dirname(__file__))
# path = os.path.join(my_path, "Scrape_Data_Times_10.csv")
#
# df = pd.read_csv(path)  ##Change the path
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', -1)
#
# ##FirstUserLogin then Content Based Model
# if (result == 'Y'):
#     print(result)
#     cursor.execute('select preferences from preferences where user_id=' + userId)
#     result = cursor.fetchone()[0]
#     print(result)
#     noOfPreferences = result.split(",")
#     print("Number of Preferences:" + str(len(noOfPreferences)))
#
#     if (len(noOfPreferences) > 1):
#         for y in noOfPreferences:
#             with open('dictionarycsv.csv', 'a+') as f:
#                 dictionary = df.loc[df['Section'] == y]
#                 # print(dictionary['Dictionary'])
#                 writetocsv = dictionary['Dictionary'].head(3)
#                 # print(writetocsv)
#                 writetocsv.to_csv(f)
#     else:
#         dictionary = df.loc[df['Section'] == noOfPreferences[0]]
#         writetocsv = dictionary['Dictionary'].head(3)
#         # print(f)
#         writetocsv.to_csv("dictionarycsv.csv", index=False)
#
#     results = ''
#
#     ##JSON FORMAT
#     with open('dictionarycsv.csv') as infile:
#         read = csv.reader(infile)
#         for row in read:
#             try:
#                 finalresult = row[1] + ","
#             except:
#                 pass
#             # finalresult = ",".join(row)
#             t = open("json.txt", "a+")
#             # t.write('[')
#             t.write(finalresult)
#             # t.write(']')
#             t.close()
#             results = results + finalresult
#
#     finalresultttt = results[:-1]
#     print(finalresultttt)
#     d = json.loads(finalresultttt)
#
#
#      ##FinalResult for Content Based
#     # os.remove('dictionarycsv.csv')
#
# else:
#     ##Collaborative Item based knn filtering
#     ##Change the path
#     df_matrix = pd.read_csv(path)
#     news_user_mat = df.pivot(index='ID', columns='Topic', values='Rating').fillna(0)
#     news_to_idx = {
#         news: i for i, news in
#         enumerate(list(df_matrix.set_index('ID').loc[news_user_mat.index].Title))
#     }
#     news_user_mat_sparse = csr_matrix(news_user_mat.values)
#     model_knn = NearestNeighbors(metric='euclidean', algorithm='auto', n_neighbors=10, n_jobs=-1)
#     model_knn.fit(news_user_mat_sparse)
#     cursor.execute('use myflaskapp')
#     cursor.execute('select news_title from user_history where user_ID=' + userId + ' order by id desc')
#     result = cursor.fetchone()
#     print(result)
#     if (result == None):
#         print("in none")
#         my_favorite = 'Drug prices must be revealed in TV ads under new Trump rule'
#     else:
#         print("in else")
#         my_favorite = result[0]
#
#     make_recommendation(model_knn=model_knn, data=news_user_mat_sparse, fav_movie=my_favorite, mapper=news_to_idx,
#                         n_recommendations=5)


def Articles():
    articles =[
        #d
        {
            "ID":"1",
            "Topic":"Entertainment",
            "Title": "The Walking Dead's Final Episode Is A Satisfying Ending",
            "Description": 'The Walking Dead: The Final Season started strong, with Telltale&rsquo;s talented storytellers crafting a compelling new scenario for Clementine to navigate. After the company&rsquo;s closure, the fate of the season looked shaky, and Skybound Games took over finishing it up.  Ultimately, the finale sticks the landing, closing...',
            "Source": 'www.kotaku.com.au',
            "Link":"http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=EA11132522D042F99D31CA1C454F71E1&url=https%3a%2f%2fwww.msn.com%2fen-us%2fmoney%2fcompanies%2fdrug-prices-must-be-revealed-in-tv-ads-under-new-trump-rule%2far-AAB67a0%3fli%3dBBnb7Kz&c=14251807532992597656&mkt=en-au",
            "Image": 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/dbbx1dnhlfqhevormf6f.jpg'
        },
        {
           "ID":"2",
            "Topic":"Business",
            "Title": "The Walking Dead's Final Episode Is A Satisfying Ending",
            "Description": 'The Walking Dead: The Final Season started strong, with Telltale&rsquo;s talented storytellers crafting a compelling new scenario for Clementine to navigate. After the company&rsquo;s closure, the fate of the season looked shaky, and Skybound Games took over finishing it up.  Ultimately, the finale sticks the landing, closing...',
            "Source": 'www.kotaku.com.au',
            "Link":"http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=EA11132522D042F99D31CA1C454F71E1&url=https%3a%2f%2fwww.msn.com%2fen-us%2fmoney%2fcompanies%2fdrug-prices-must-be-revealed-in-tv-ads-under-new-trump-rule%2far-AAB67a0%3fli%3dBBnb7Kz&c=14251807532992597656&mkt=en-au",
            "Image": 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/dbbx1dnhlfqhevormf6f.jpg'
        },
        {
            "ID":"3",
            "Topic":"Health",
            "Title": "The Walking Dead's Final Episode Is A Satisfying Ending",
            "Description": 'The Walking Dead: The Final Season started strong, with Telltale&rsquo;s talented storytellers crafting a compelling new scenario for Clementine to navigate. After the company&rsquo;s closure, the fate of the season looked shaky, and Skybound Games took over finishing it up.  Ultimately, the finale sticks the landing, closing...',
            "Source": 'www.kotaku.com.au',
            "Link":"http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=EA11132522D042F99D31CA1C454F71E1&url=https%3a%2f%2fwww.msn.com%2fen-us%2fmoney%2fcompanies%2fdrug-prices-must-be-revealed-in-tv-ads-under-new-trump-rule%2far-AAB67a0%3fli%3dBBnb7Kz&c=14251807532992597656&mkt=en-au",
            "Image": 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/dbbx1dnhlfqhevormf6f.jpg'
        },
        {
             "ID":"4",
            "Topic":"Technology",
            "Title": "The Walking Dead's Final Episode Is A Satisfying Ending",
            "Description": 'The Walking Dead: The Final Season started strong, with Telltale&rsquo;s talented storytellers crafting a compelling new scenario for Clementine to navigate. After the company&rsquo;s closure, the fate of the season looked shaky, and Skybound Games took over finishing it up.  Ultimately, the finale sticks the landing, closing...',
            "Source": 'www.kotaku.com.au',
            "Link":"http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=EA11132522D042F99D31CA1C454F71E1&url=https%3a%2f%2fwww.msn.com%2fen-us%2fmoney%2fcompanies%2fdrug-prices-must-be-revealed-in-tv-ads-under-new-trump-rule%2far-AAB67a0%3fli%3dBBnb7Kz&c=14251807532992597656&mkt=en-au",
            "Image": 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/dbbx1dnhlfqhevormf6f.jpg'
        },
        {
            "ID":"5",
            "Topic":"Sports",
            "Title": "The Walking Dead's Final Episode Is A Satisfying Ending",
            "Description": 'The Walking Dead: The Final Season started strong, with Telltale&rsquo;s talented storytellers crafting a compelling new scenario for Clementine to navigate. After the company&rsquo;s closure, the fate of the season looked shaky, and Skybound Games took over finishing it up.  Ultimately, the finale sticks the landing, closing...',
            "Source": 'www.kotaku.com.au',
            "Link":"http://www.bing.com/news/apiclick.aspx?ref=FexRss&aid=&tid=EA11132522D042F99D31CA1C454F71E1&url=https%3a%2f%2fwww.msn.com%2fen-us%2fmoney%2fcompanies%2fdrug-prices-must-be-revealed-in-tv-ads-under-new-trump-rule%2far-AAB67a0%3fli%3dBBnb7Kz&c=14251807532992597656&mkt=en-au",
            "Image": 'https://i.kinja-img.com/gawker-media/image/upload/c_lfill,w_768,q_90/dbbx1dnhlfqhevormf6f.jpg'
        }
    ]
    return articles