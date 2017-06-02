import time
import urllib2
from bs4 import BeautifulSoup
import os
import pymongo
import settings

connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION_BIGDATA']]



querys = collection.find()
print len(querys)