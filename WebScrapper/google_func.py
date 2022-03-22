import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import WebScrapper.date_func as d
import WebScrapper.link_preview as lp
import json

def google_func(res):
    pubdate = datetime.datetime.strptime(res.pubDate.text, "%a, %d %b %Y %H:%M:%S %Z")
    pubdate = datetime.datetime.strftime(pubdate,"%Y-%m-%d %H:%M:%S")
    pubdate = datetime.datetime.strptime(pubdate,"%Y-%m-%d %H:%M:%S")
    title = str(res.title.text)
    link = str(res.link.text)
    pubdate_str = datetime.datetime.strftime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
    a = lp.generate_dict(link)
    try:
    	source = res.source.text
    except:
    	source = "Null"
    title = title.replace("'", '"')
    link = link.replace("'", '"')
    source = source.replace("'", '"')
    image = image.replace("'", '"')
    description = description.replace("'", '"')

    if d.weekOld(pubdate) < 0:
        return 0
    else:
        return [title, pubdate, link, image, description, source]