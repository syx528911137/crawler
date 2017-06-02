#-*-coding:UTF-8-*-
import scrapy
from scrapy.selector import Selector
from crawlnews.items import CrawlnewsItem
import time
import random
import urllib2
from crawlnews.ValidateIP import ValidateIP
import crawlnews.settings as settings
import pymongo
from bs4 import BeautifulSoup

class SpiderSina(scrapy.Spider):
    name = "ittime"
    allowed_domains = ["ittime.com.cn"]
    startURL = "http://www.ittime.com.cn/newslist.shtml"



    def __init__(self,time):
        self.time = int(time)
        # self.mongodb_host = settings.MONGODB_HOST
        # self.mongodb_port = settings.MONGODB_PORT
        # self.mongo_connection = pymongo.MongoClient(self.mongodb_host, self.mongodb_port)
        # self.conn = self.mongo_connection['proxyIP']
        # self.db = self.conn['ips']
        # self.USER_AGENT = [ \
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        #     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        #     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        #     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        #     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        # ]


    #
    # def get_proxyip(self):
    #     PROXIES = []
    #     tmp_proxy = self.db.find()
    #     for ip in tmp_proxy:
    #         tmp = ip['ip'] + ":" + ip['port']
    #         PROXIES.append(tmp)
    #     ip = random.choice(PROXIES)
    #     v = ValidateIP()
    #     while ~v.check(ip.split(":")[0],ip.split(":")[1]):
    #         ip = random.choice(PROXIES)
    #     return ip


    def getResponse(self,url):
        # tmp_proxy = self.get_proxyip()  # daili ip
        # # print tmp_proxy
        # # url = 'http://ip.catr.cn/'
        # user_agent = random.choice(self.USER_AGENT)
        # proxy = {'http': tmp_proxy}
        # headers = [('User-Agent', user_agent)]
        # proxy_s = urllib2.ProxyHandler(proxies=proxy)
        # opener = urllib2.build_opener(proxy_s)
        # opener.addheaders = headers
        # req = opener.open(url, data=None)




        # str =/
        #
        #
        print "getResponse:"  + url
        req = urllib2.urlopen(url)
        return req.read()







    def start_requests(self):
        # url = "http://www.ittime.com.cn/newslist_94.shtml"
        #
        # yield scrapy.FormRequest(url,dont_filter=True,callback=self.processNewsUrls)
        # print "start_requests"
        # return [scrapy.FormRequest(self.startURL,callback=self.processPageInfo)]
        #******************************************************************************
        resp = self.getResponse(self.startURL)
        sel = Selector(text=resp)
        pages = sel.xpath('//div[@class="page"]').extract()[0]
        bp = BeautifulSoup(pages,'lxml')
        pageBox = bp.get_text().split(' ')
        print pageBox
        ele = str(pageBox[len(pageBox) - 2])
        print "--------------------------------------"
        print ele
        pageNum = 100
        try:
            ele = ele.replace('..','')
            pageNum = int(ele)
        except:
            # pageNum = 100
            pass

        print "********************************************************"
        print pageNum
        # time.sleep(1000)
        for i in xrange(1, pageNum + 1):
            print "processPageInfo"
            urlFirst = "http://www.ittime.com.cn/newslist.shtml"
            urlHead = "http://www.ittime.com.cn/newslist_"
            urlTail = ".shtml"
            url = ""
            if i == 1:
                url = urlFirst
            else:
                url = urlHead + str(i) + urlTail


            # url = "http://roll.tech.sina.com.cn/s/channel.php?ch=05#col=30&spec=&type=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=" + str(i)
            # if i == 2:
            #     break
            yield scrapy.FormRequest(url=url, callback=self.processNewsUrls)
    #***************************************************************************************************




    def processNewsUrls(self,response):
        # print "-------------------------------------------------------------"
        if str(response.url) != "http://news.ittime.com.cn/about/404.html":
            # print "*****************************************************************"
            print response.url
            sel = Selector(response)
            newsURLlists = sel.xpath('//dl[@class="newsList"]').extract()
            print len(newsURLlists)
            # time.sleep(100)
            for i in range(0,len(newsURLlists)):
                # if i == 1:
                #     break

                tmp = Selector(text=newsURLlists[i])
                url = tmp.xpath('//dt/a/@href').extract()
                label = tmp.xpath('//dt/div/text()').extract()
                secondS = tmp.xpath('//dd/div/span[@class="pull-left from_ori"]/text()').extract()
                print "processNewsList"
                # print url[0]
                # print label[0]
                # time.sleep(1000)
                t = tmp.xpath('//dd/div/span/span[@class="year"]/text()').extract()[0]
                tmp_time = int(t.split(' ')[0].replace('-',''))
                # print "-----------------------------------------------------------***************************"
                # print tmp_time
                # time.sleep(1000)
                if tmp_time > self.time:





                    # label = tmp.xpath('//dt/div/text()').extract()[0]
                    request_url = "http://www.ittime.com.cn" + url[0]
                    print request_url
                    # time.sleep(10000)
                    yield scrapy.FormRequest(url=request_url,meta={'label':label[0],'secondSource':secondS[0]},callback=self.processNews)


    def processNews(self,response):
        print "processNews"
        sel = Selector(response)
        item = CrawlnewsItem()
        item['title'] = sel.xpath('/html/body/div[1]/div/div[1]/div/h2/text()').extract()[0]
        item['time'] = sel.xpath('//div[@class="left_main"]/div/span[@class="time"][2]/text()').extract()[0]
        newlist = sel.xpath('//div[@class="left_main"]/p/text()').extract()
        news = ""
        for i in range(0,len(newlist)):
            news = news + newlist[i] + " "
            # print news
        news = news.strip()
        item['content'] = news
        item['kind'] = response.meta.get('label')
        # labs = sel.xpath('//*[@id="wrapOuter"]/div[2]/div[4]/p/a/text()').extract()
        # label = ""
        # for j in range(0,len(labs)):
        #     label = label + labs[j] + " "
        # label = label.strip()
        item['labels'] = response.meta.get('label')
        item['firstSource'] = 'ittime'
        item['secondSource'] = response.meta.get('secondSource')
        print "processNews*************************************************************************"
        # print item
        # time.sleep(1000)
        yield item



