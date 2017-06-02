#-*-coding:UTF-8-*-
import scrapy
from scrapy.selector import Selector
from crawlnews.items import CrawlPaperItem
import time
import random
import urllib2
from crawlnews.ValidateIP import ValidateIP
import crawlnews.settings as settings
import pymongo
from bs4 import BeautifulSoup
from crawlnews.pipelines import CrawlPaperPipeline

class SpiderSina(scrapy.Spider):
    name = "paper"
    allowed_domains = ["arxiv.org"]

    custom_settings = {
        'ITEM_PIPELINES':{
   # 'crawlnews.pipelines.CrawlnewsPipeline': 300,
   'crawlnews.pipelines.CrawlPaperPipeline':301,
        }
    }
    # pipeline = set([CrawlPaperPipeline,])

    def start_requests(self):
        pre_url = "https://arxiv.org/list/cs/16?skip=0&show=1000"
        resp = urllib2.urlopen(pre_url)
        html = resp.read()
        bup = BeautifulSoup(html, 'lxml')
        num = str(bup.small).split(':')[0].split(' ')
        # print len(total_number)
        # print total_number
        totalNum = 0
        for i in num:
            try:
                totalNum = int(i)
            except:
                pass
        begin_cs = 0
        while begin_cs < totalNum:
            url = "https://arxiv.org/list/cs/16?skip=" + str(begin_cs) + "&show=25"
            begin_cs = begin_cs + 25
            yield scrapy.FormRequest(url=url,meta={'type':'cs'},callback=self.processPaperUrlList)
            # break




    def processPaperUrlList(self,response):
        sel = Selector(response)
        type = response.meta.get('type')
        urls = sel.xpath('//div[@id="dlpage"]/dl/dt/span/a[1]/@href').extract()
        for tmp in urls:
            url = "https://arxiv.org" + tmp
            print "************:" + url
            yield scrapy.FormRequest(url,meta={'type':type},callback=self.processPaper)
            # break



    def processPaper(self,response):
        sel = Selector(response)
        item = CrawlPaperItem()
        item['title'] = sel.xpath('//div[@id = "abs"]/div[@class="leftcolumn"]/h1/text()').extract()
        if type(item['title']) == type([]):
            item['title'] = item['title'][0]
        tmp_author = sel.xpath('//div[@id = "abs"]/div[@class="leftcolumn"]/div[@class="authors"]/a/text()').extract()
        item['author'] = ''
        for tmp in tmp_author:
            item['author'] = item['author'] + tmp
        tmp_abs_html = sel.xpath('//div[@id = "abs"]/div[@class="leftcolumn"]/blockquote').extract()[0]
        # print tmp_abs_html
        bup = BeautifulSoup(tmp_abs_html,'lxml')
        item['abstract'] = bup.getText()
        tmp_tr_list = sel.xpath('//div[@class="metatable"]/table/tr').extract()
        # print "tmp_tr_list:"
        # print tmp_tr_list
        subject = ''
        for tr in tmp_tr_list:
            s = Selector(text=tr)
            tmp_sub = s.xpath('//td[1]/text()').extract()[0]
            # print "***********************************************"
            # print type(tmp_sub.lower().strip())
            # print type(u"subjects:")
            # print tmp_sub.lower().strip() == u"subjects:"
            # print tmp_sub == u'Subjects:'
            if tmp_sub.lower().strip() == u"subjects:":
                tmp_html = s.xpath('//td[2]').extract()[0]
                tmp_bp = BeautifulSoup(tmp_html,'lxml')
                subject = tmp_bp.getText()
                print "--------------------------------------------"
                print subject
        item['subjects'] = subject
        yield item
