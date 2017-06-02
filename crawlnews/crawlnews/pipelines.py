# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import settings
import pymongo

class CrawlnewsPipeline(object):
    def __init__(self):
        self.mongodb_host = settings.MONGODB_HOST
        self.mongodb_port = settings.MONGODB_PORT
        self.mongo_connection = pymongo.MongoClient(self.mongodb_host,self.mongodb_port)
        self.conn = self.mongo_connection['news']
        self.db = self.conn['keji']



    def process_item(self, item, spider):
        print "********************************pipeline*********************************************"

        news = {}
        news['title'] = item['title'][0]
        news['time'] = item['time'][0]
        news['content'] = item['content']
        news['kind'] = item['kind']
        news['labels'] = item['labels']
        self.db.insert(news)
        print item
        return item



class CrawlPaperPipeline(object):
    def __init__(self):
        self.mongodb_host = settings.MONGODB_HOST
        self.mongodb_port = settings.MONGODB_PORT
        self.mongo_connection = pymongo.MongoClient(self.mongodb_host, self.mongodb_port)
        self.conn = self.mongo_connection['paper']
        self.db = self.conn['paper']
        pass
    def process_item(self,item,spider):
        print "*****************************paper****************************"
        paper = {}
        paper['title'] = item['title']
        paper['abstract'] = item['abstract']
        paper['author'] = item['author']
        paper['subjects'] = item['subjects']
        self.db.insert(paper)
        return item
        pass