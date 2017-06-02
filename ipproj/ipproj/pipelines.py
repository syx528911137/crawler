# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
# from scrapy.pipelines.images import ImagesPipeline
import datetime
import logging
# import ipproj.settings as ipsettings
from ipproj.decorator import check_spider_pipeline
#写图片需要的库
import urllib

import os

# class TestprojPipeline(object):
#     def process_item(self, item, spider):
#         return item

class ImageDownloadPipeline(object):

    # def get_media_requests(self, item, info):#重写ImagesPipeline   get_media_requests方法
    #     '''
    #     :param item:
    #     :param info:
    #     :return:
    #     在工作流程中可以看到，
    #     管道会得到文件的URL并从项目中下载。
    #     为了这么做，你需要重写 get_media_requests() 方法，
    #     并对各个图片URL返回一个Request:
    #     '''
    #     print "======================"
    #     if item['image_urls'] == ['']:
    #         raise DropItem("no picture")
    #     dir_path = settings.IMAGES_STORE + '/'
    #     if not os.path.exists(dir_path):
    #         os.makedirs(dir_path)
    #     us = item['image_urls'].split('/')[-1]
    #     file_path = dir_path + us 
    #     print "*********************"
    #     print file_path
    #     print "*********************"
    #     if os.path.exists(file_path):
    #         pass
    #     else:
    #         urllib.urlretrieve("http://epub.sipo.gov.cn/" + item['image_urls'],file_path)#写图片的

    #     yield scrapy.Request(''.join(item['image_urls']))

 
    # def item_completed(self, results, item, info):
    #     '''
 
    #     :param results:
    #     :param item:
    #     :param info:
    #     :return:
    #     当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败），
    #      item_completed() 方法将被调用。
    #     '''
    #     # print "22333333"

    #     print results
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     # print "*********************"
    #     # print image_paths
    #     # print "*********************"
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     # urllib.urlretrieve("http://epub.sipo.gov.cn/" + item['image_urls'],image_paths)#写图片的
    #     item['file_paths'] = image_paths
    #     return item

        
    def process_item(self, item, spider):
        if item['image_urls'] == '':
            return item
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        dir_path = settings['IMAGES_STORE'] + spider.name + '/' + date + '/full/'
        dir_thumb_path = settings['IMAGES_STORE'] + spider.name + '/' + date + '/thumb/'

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(dir_thumb_path):
            os.makedirs(dir_thumb_path)
        us = item['authId'] + '.jpg'
        file_path = dir_path + us 
        file_thumb_path = dir_thumb_path + us 

        if os.path.exists(file_path):
            pass
        else:
            urllib.urlretrieve("http://epub.sipo.gov.cn/" + item['image_urls'],file_path)#写图片的
            print file_path
            urllib.urlretrieve("http://epub.sipo.gov.cn/" + item['image_thumb_urls'],file_thumb_path)#写图片的
            # print "=======================" +item['image_urls']
        item['image_urls'] = file_path
        item['image_thumb_urls'] = file_thumb_path

        return item


class MongoDBBigdataPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_BIGDATA']]
        pass

    @check_spider_pipeline
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data['title']))
        if valid:
            # self.collection.insert(dict(item))
            temp = self.collection.find_one(dict(item))

            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")

            if temp is not None:
                logging.info(otherStyleTime + " item is already exist! " + item["authId"])
                #i = dict(item)
                #i['_id'] = temp['_id']
                #self.collection.save(i)
            else:
                logging.info(otherStyleTime + " item is not exist! " + item["authId"])
                self.collection.insert(dict(item))
                # log.msg("Patent info added to MongoDB database!",
                #             level=log.DEBUG, spider=spider)
            logging.info("Patent info added to MongoDB database!")
        return item


class JsonPipeline1(object):
    def __init__(self):
        self.file = codecs.open('ip1.json','w', encoding='utf-8')

    @check_spider_pipeline
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class JsonPipeline2(object):
    def __init__(self):
    	self.file = codecs.open('ip2.json','w', encoding='utf-8')

    @check_spider_pipeline
    def process_item(self, item, spider):
    	line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    	self.file.write(line)
        return item
    def spider_closed(self, spider):
    	self.file.close()


class MongoDBFmgbPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_FMGB']]
        pass

    @check_spider_pipeline
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data['title']))
        if valid:
            # self.collection.insert(dict(item))
            temp = self.collection.find_one(dict(item))

            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
            
            if(temp):
                logging.info( otherStyleTime + " item is already exist! "+ item["authId"])
                i = dict(item)
                i['_id']=temp['_id']
                self.collection.save(i)
            else:
                logging.info( otherStyleTime + " item is not exist! " + item["authId"])
                self.collection.insert(dict(item))
            # log.msg("Patent info added to MongoDB database!",
        #             level=log.DEBUG, spider=spider)
            logging.info("Patent info added to MongoDB database!")
        return item


class MongoDBFmsqPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_FMSQ']]
        pass

    @check_spider_pipeline
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data['title']))
        if valid:
            # self.collection.insert(dict(item))
            temp = self.collection.find_one(dict(item))

            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
            
            if(temp):
                logging.info( otherStyleTime + " item is already exist! "+ item["authId"])
                i = dict(item)
                i['_id']=temp['_id']
                self.collection.save(i)
            else:
                logging.info( otherStyleTime + " item is not exist! " + item["authId"])
                self.collection.insert(dict(item))
            logging.info( "Patent info added to MongoDB database!")
            
        return item

class MongoDBXxsqPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_XXSQ']]
        pass

    @check_spider_pipeline
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data['title']))
        if valid:
            # self.collection.insert(dict(item))
            temp = self.collection.find_one(dict(item))

            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
            
            if(temp):
                logging.info( otherStyleTime + " item is already exist! "+ item["authId"])
                i = dict(item)
                i['_id']=temp['_id']
                self.collection.save(i)
            else:
                logging.info( otherStyleTime + " item is not exist! " + item["authId"])
                self.collection.insert(dict(item))
            logging.info( "Patent info added to MongoDB database!")
        return item

class MongoDBWgsqPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_WGSQ']]
        pass

    @check_spider_pipeline
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Dropping  %s!" % data['authId'])
        if valid:
            # self.collection.insert(dict(item))
            temp = self.collection.find_one(dict(item))

            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
            
            if(temp):
                logging.info( otherStyleTime + " item is already exist! "+ item["authId"])
                i = dict(item)
                i['_id']=temp['_id']
                self.collection.save(i)
            else:
                logging.info( otherStyleTime + " item is not exist! " + item["authId"])
                self.collection.insert(dict(item))
            logging.info( "Patent info added to MongoDB database!")
        return item
