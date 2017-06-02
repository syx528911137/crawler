import pymongo
import urllib
import re
import time
import redis
from bs4 import BeautifulSoup
import sys
import random


mongodb_host = '127.0.0.1'
mongodb_port = 27017
mongo_connection = pymongo.MongoClient(mongodb_host,mongodb_port)
conn = mongo_connection['paper']
db_paper = conn['paper_containletter_a']
r = redis.Redis(host='localhost',port=6379)


url = 'http://export.arxiv.org/api/query?search_query=all:t&start=0&max_results=1'
data = urllib.urlopen(url).read()
# print data
matchObj = re.search(r'totalResults .*?>(\d*)',data,re.M|re.I)
# if matchObj:
all_num = int(matchObj.group(1))


print all_num



start = int(sys.argv[1])
skip = int(sys.argv[2])
xunhuan = 0
while start < all_num:
    if xunhuan == 8:
        start = start + random.randint(0,skip)
        xunhuan = 0
        continue
    # if start != 0:0
    #     break
    xunhuan = xunhuan + 1
    url = 'http://export.arxiv.org/api/query?search_query=all:t&start=' + str(start) + '&max_results='+str(skip)
    print url
    start = start + skip
    data = urllib.urlopen(url).read()
    bsp = BeautifulSoup(data,'lxml')
    paperList = bsp.find_all('entry')
    if len(paperList) == 0:
        start = start - skip
        print start
        continue
    for entry in paperList:
        xunhuan = 0
        paper = {}
        paper['title'] = entry.find('title').getText()
        authorsList = entry.find_all('name')
        authors = ''
        for tmp_a in authorsList:
            authors = authors + tmp_a.getText()
        paper['author'] = authors
        paper['abstract'] = entry.find('summary').getText()
        # matchObj = re.search(r'category.*term="(.*)"',entry.prettify())

        paper['category'] = entry.find('category')['term']
        paper['publicTime'] = entry.find('published').string
        paper['updateTime'] = entry.find('updated').string

        if r.sadd('paper-dupefilter',paper['title']):
            db_paper.insert(paper)
            print "save..."
        else:
            print "exsit..."
            pass

    # time.sleep(5)