# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib2
from bs4 import BeautifulSoup
from crawlIP.ValidateIP import ValidateIP

class CrawlipPipeline(object):

    def process_item(self, item, spider):


        print "*************************************pipeline*********************************"
        proxy_ip = {}
        proxy_ip['host'] = item['host']
        proxy_ip['port'] = item['port']
        proxy_ip['kind'] = item['kind']
        # print proxy_ip
        validate = ValidateIP()
        flag = validate.check(proxy_ip['host'],proxy_ip['port'])
        if flag == True:
            print "*******************************************you xiao************************************"


        return item
