import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import requests
import datetime
import pytz

import numpy as np
import json
import link_preview as lp
import WebScrapper.date_func as d
import WebScrapper.google_func as google
import WebScrapper.bing_func as bing
import WebScrapper.abc_func as abc
import WebScrapper.Links

categories = WebScrapper.Links.categories
df1 = pd.DataFrame(columns=['ID', 'Title', 'Topic', 'Section', 'Timestamp', 'RSS', 'Link', 'Image', 'Description', 'Source'])
i = 0
# a = [categories, df1, i]
def scrape_task(categories, df1, i):
	jsonDict = []
	for topic, topic_dict in categories.items():
		for section, section_link in topic_dict.items():
				for key, val in section_link.items():
					try:
						r = requests.get(val)
						soup = BeautifulSoup(r.content, features = 'xml')
						for res in soup.findAll('item'):
						    if key == 'Bing':
						    	data = bing.bing_func(res)
						    	bingstatus = r.status_code
						    elif key == 'ABC':
						    	data = abc.abc_func(res)
						    elif key == 'Google':
						    	if bingstatus == requests.codes.ok:
						    		data = 0
						    	else:
						    		data = google.google_func(res)
						    try:
						    	if data != 0:
						    		df1.loc[i] =[i, data[0], topic, section, data[1], key, data[2], data[3], data[4], data[5]]
						    	else:
						    		pass				    	
						    except Exception as e:
						    	print("Didn't write")
						    i+=1			    
					except:
						pass
	df1.sort_values(by="Timestamp", ascending=False,inplace = True)
	df1.reset_index(inplace=True, drop=True)
	df1['ID'] = df1.index.tolist()

	new_list = []
	for k, rows in df1.iterrows():
		new_list.append(rows['Section'])
	a = Counter(new_list)
	for i, j in a.items():
		k = (j/len(new_list))*100
		df1.loc[df1['Section'] == i,'Rating'] = int(round(k, 0))
	for k, rows in df1.iterrows():
		jdict = {
			"ID": rows["ID"],
			"Title": rows["Title"].strip(),
			"Topic": rows["Topic"].strip(),
			"Section": rows["Section"].strip(),
			"Timestamp": str(rows["Timestamp"]).strip(),
			"RSS": rows["RSS"].strip(),
			"Link": rows["Link"].strip(),
			"Image": rows["Image"].strip(),
			"Description": rows["Description"].strip(),
			"Source": rows["Source"].strip(),
			"Rating": rows["Rating"]
		}
		jdict = json.dumps(jdict, indent=4)
		jsonDict.append(jdict)
	df1['JsonDict'] = jsonDict

	df2 = df1.filter(['ID', 'Title', 'Rating'], axis=1)
	try:
		df1.to_csv("Scrape_Data.csv")
	except:
		print("Could not write Scrape Data to CSV file. Please ensure that it is not locked for editing")
	try:
		df2.to_csv("Scrape_Data_Lite.csv")
	except:
		print("Could not write Scrape Data Lite to CSV file. Please ensure that it is not locked for editing")

def scrape():
	print("Starting scrape...")
	scrape_task(categories, df1, i)

# scrape()

# s.every(3).minutes.do(scrape_task, [categories, df1, i]) 	