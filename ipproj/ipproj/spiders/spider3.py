# -*- coding: utf-8 -*-
import scrapy
from ipproj.items import IpprojItem
from ipproj import pipelines
from scrapy.selector import Selector
from scrapy.conf import settings
import scrapy_redis.connection as connection
from scrapy.exceptions import DropItem
# from ipproj.spiders.dateutil import dateutil
import random
import math
import logging
import time

class Spider3Spider(scrapy.Spider):
    name = "spider3"
    allowed_domains = ["epub.sipo.gov.cn"]

    date = ""
    pageNumber = 0
    ptype = "xxsq"
    key=name


    def __init__(self, date):
        self.pageNumber = 0
        self.date = "PD=" + date
        self.server = connection.from_settings(settings)
        
    pipeline = set([
        # pipelines.JsonPipeline2,
        pipelines.MongoDBXxsqPipeline,
    ])

    def start_requests(self):
        # util = dateutil()
        # dateList = util.getAllWed()
        # for index,d in enumerate(dateList):
        #     dateList[index] = "公开（公告）日="+d
        # for d in dateList:
        #     print d
        # self.date = "公开（公告）日=2016.06.22"
        yield scrapy.FormRequest("http://epub.sipo.gov.cn/patentoutline.action",
            formdata={'showType': '1', 'strWhere': self.date, 'numSortMethod': '5', 'strLicenseCode': '', 'numIp': '', 'numIpc': '', 'numIg': '', 'numIgc': '', 'numIgd': '', 'numUg': '0', 'numUgc': '', 'numUgd': '', 'numDg': '', 'numDgc': '',
               'pageSize': '10', 'pageNow': '1'},
            meta={'type': self.ptype},
            callback=self.post_over)
        pass

    def post_over(self, response):
        if self.pageNumber == 0:
            self.pageNumber = self.server.get("PageNumber-"+self.date+"-"+self.ptype)
        if(self.pageNumber == None):
            logging.info("pageNumber need to wait 3 seconds")
            time.sleep(3)
            hxs = Selector(response)
            #scrapy.shell.inspect_response(response,self)
            self.pageNumber = hxs.xpath('//div[@class="next"]/a[7]/text()').extract()[0]
            self.server.set("PageNumber-"+self.date+"-"+self.ptype,self.pageNumber)
        for i in xrange(1, int(self.pageNumber) + 1):
            yield scrapy.FormRequest("http://epub.sipo.gov.cn/patentoutline.action",
                formdata={'showType': '1', 'strWhere': self.date, 'numSortMethod': '5', 'strLicenseCode': '', 'numIp': '', 'numIpc': '', 'numIg': '', 'numIgc': '', 'numIgd': '', 'numUg': '0', 'numUgc': '', 'numUgd': '', 'numDg': '', 'numDgc': '',
                   'pageSize': '10', 'pageNow': str(i)},
                meta={'type': self.ptype,
                    'page': str(i)},
                callback=self.post_detail)

    def post_detail(self, response):
        items = []
        page = response.meta.get('page',None)
        hxs = Selector(response)
        patents = hxs.xpath('//div[@class="cp_box"]')
        if len(patents) == 0:
            logging.error("this page was blocked, try to read again. page number is " + page + ", type is " + self.ptype)
            time.sleep(120)
            scrapy.FormRequest(
                "http://epub.sipo.gov.cn/patentoutline.action",
                formdata={'showType': '1', 'strWhere': self.date, 'numSortMethod': '5', 'strLicenseCode': '', 'numIp': '', 'numIpc': '', 'numIg': '', 'numIgc': '', 'numIgd': '', 'numUg': '0', 'numUgc': '', 'numUgd': '', 'numDg': '', 'numDgc': '',
                    'pageSize': '10', 'pageNow': str(page)},
                dont_filter=True,
                meta={'type': self.ptype,
                    'page': page},
                callback=self.post_detail
            )
        for box in patents:
            item = IpprojItem()
            item['type'] = response.meta.get('type', None)
            item['title'] = box.xpath(
                'div[@class="cp_linr"]/h1[1]/text()').extract()[0].replace(u'\r\n\t\t\t\t[发明公布] ', '')
            # authId    授权号
            item['authId'] = box.xpath(
                '''div[@class="cp_linr"]/ul/li[@class="wl228"][1]/text()''').extract()[0].replace(u'申请公布号：', '')  # 授权公告号
            # authDate  授权日
            item['authDate'] = box.xpath(
                'div[@class="cp_linr"]/ul/li[@class="wl228"][2]/text()').extract()[0].replace(u'申请公布日：', '')  # 授权公告日：
            # appId     申请号
            item['appId'] = box.xpath(
                'div[@class="cp_linr"]/ul/li[@class="wl228"][3]/text()').extract()[0].replace(u'申请号：', '')
            # appDate   申请日
            item['appDate'] = box.xpath(
                'div[@class="cp_linr"]/ul/li[@class="wl228"][4]/text()').extract()[0].replace(u'申请日：', '')
            # appOwner  申请人
            item['appOwner'] = box.xpath(
                'div[@class="cp_linr"]/ul/li[@class="wl228"][5]/text()').extract()[0].replace(u'申请人：', '')  # 专利权人：
            # 专利图片
            item['image_thumb_urls'] = box.xpath(
                'div[@class="cp_img"]/img/@src').extract()[0]

            if item['image_thumb_urls'] != "images/cp_noimg.jpg":
                item['image_urls'] = item[
                    'image_thumb_urls'].replace('_thumb', '')
            else:
                item['image_urls'] = ''
                item['image_thumb_urls'] = ''


            owner2 = box.xpath(
                'div[@class="cp_linr"]/ul/li[@class="wl228"][5]/div[@style="display:none;"]/text()').extract()
            if (owner2):
                item['appOwner2'] = owner2[0]
            # inventor  发明人 可能有多个
            item['inventor'] = box.xpath(
                'div[@class="cp_linr"]/ul/li[@class="wl228"][6]/text()').extract()[0].replace(u'发明人：', '')
            inventors2 = box.xpath(
                'div[@class="cp_linr"]/ul/li[@class="wl228"][6]/div[@style="display:none;"]/text()').extract()
            if len(inventors2) > 0:
                item['inventor2'] = inventors2[0]
            # address   地址
            item['address'] = box.xpath(
                'div[@class="cp_linr"]/ul/li[8]/text()').extract()[0].replace(u'地址：', '')
            # catId     分类号
            item['catId'] = box.xpath(
                'div[@class="cp_linr"]/ul/li[9]/text()').extract()[0].replace(u'分类号：', '')
            # 还有分类号，代理机构名称等等
            otherDetail = box.xpath(
                'div[@class="cp_linr"]/ul/li[9]/div[@style="display:none;"]/ul/li/text()').extract()
            item['otherDetail'] = otherDetail
            # abstract  摘要
            abstracts = box.xpath(
                'div[@class="cp_linr"]/div[@class="cp_jsh"][1]/text()').extract()[1]
            abstracts2 = box.xpath(
                'div[@class="cp_linr"]/div[@class="cp_jsh"]/span[@style="display:none;"]/text()').extract()
            item['abstract'] = abstracts

            if len(abstracts2) > 0:
                item['abstract'] = abstracts.replace(
                    '\r\n\t\t\t\t', '') + abstracts2[0]
            else:
                item['abstract'] = abstracts.replace('\r\n\t\t\t\t', '')
            
            strWhere= 'PN=' + item['authId']

            # yield scrapy.FormRequest("http://epub.sipo.gov.cn/pam.action",
            #                         formdata={
            #                              'strSources': 'pip', 'strWhere': strWhere, 'recordCursor': '0'},
            #                         meta={'item':item,
            #                          'value':value},
            #                         dont_filter=True,
            #                         callback=self.post_link)
            items.append(item)
        return items

    def post_link(self, response):
        logging.info("23333")
        # scrapy.shell.inspect_response(response,self)
        items = []
        hxs = Selector(response)
        item = response.meta.get('item', None)

        # value = response.meta.get('value', None)

        temp = hxs.xpath('//div[@class="main"]/dl/dd/ul/li[3]/a/@href').extract()
        #有时候会有问题
        if hxs.xpath('//div[@class="main"]/dl/dd/ul/li[3]/a/@href').extract() != []:
            item['downloadlink'] = temp[0]
        elif hxs.xpath('//div[@class="main"]/dl/dd/ul/li[4]/a/@href').extract() != []:
            item['downloadlink'] = hxs.xpath('//div[@class="main"]/dl/dd/ul/li[4]/a/@href').extract()[0]
        else:
            logging.info(item['authId'])
            logging.info("###################"+value)
            logging.error(item['authId'] + "can not get downloadlink")
            item['downloadlink'] = item['authId'] + " can not get downloadlink"
            return item
            # scrapy.shell.inspect_response(response,self)

        # if temp == []:
        #     item['downloadlink'] = hxs.xpath('//div[@class="main"]/dl/dd/ul/li[4]/a/@href').extract()[0]
        # else:
        #     item['downloadlink'] = temp[0]


        logging.info(item['downloadlink']+"=====================")
        items.append(item)

        # my_server.r.sadd(self.key, value)

        return item