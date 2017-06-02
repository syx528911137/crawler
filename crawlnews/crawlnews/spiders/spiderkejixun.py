#-*-coding:UTF-8-*-
import scrapy
from scrapy.selector import Selector
import urllib2
import crawlnews.settings as settings
import pymongo
import random
from crawlnews.ValidateIP import ValidateIP
from crawlnews.items import CrawlnewsItem
import time
from bs4 import BeautifulSoup
from crawlnews.pipelines import CrawlnewsPipeline

class SpiderSina(scrapy.Spider):
    name = "kejixun"
    allowed_domains = ["kejixun.com"]

    pipeline = set([CrawlnewsPipeline,])


    def __init__(self,time):
        self.time = int(time)
    #     self.mongodb_host = settings.MONGODB_HOST
    #     self.mongodb_port = settings.MONGODB_PORT
    #     self.mongo_connection = pymongo.MongoClient(self.mongodb_host, self.mongodb_port)
    #     self.conn = self.mongo_connection['proxyIP']
    #     self.db = self.conn['ips']
    #     self.USER_AGENT = [ \
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







    def start_requests(self):
        print "start_requests"
        yield scrapy.FormRequest(url='http://www.kejixun.com/news/',dont_filter=True,callback=self.processSubKindUrls)


    def processSubKindUrls(self,response):
        print "processSubKindUrls"
        sel = Selector(response)
        urls = sel.xpath('//div[@class="blk2-tab clearfix mb20"]/a/@href').extract()
        for url in urls:
            print url
            # time.sleep(1000)
            yield scrapy.FormRequest(url=url,callback=self.processAllPagesOfSubKind)
            # break


    def processAllPagesOfSubKind(self,response):
        sel = Selector(response)
        print "processAllPagesOfSubKind"
        # time.sleep(1000)
        page = sel.xpath('//div[@class="pageList"]/div[@class="pages"]/a/text()').extract()
        pageNum = 90
        try:
            pageNum = int(page[len(page) - 2])
        except:
            pass
            # pageNum = 90
        # urls = sel.xpath('//div[@class="pageList"]/dl/dd/h2/a/@href').extract()
        urls = sel.xpath('//div[@class="pageList"]/dl').extract()
        for item in urls:
            s = Selector(text=item)
            labellist = s.xpath('//dd/p[2]/span[2]/a/text()').extract()
            url = s.xpath('//dd/h2/a/@href').extract()[0]
            labels = ""
            for i in range(1, len(labellist)):
                labels = labels + labellist[i] + " "
            labels = labels.strip()
            yield scrapy.FormRequest(url, meta={'label': labels}, callback=self.processNews)
            # break





        for i in range(2,pageNum + 1):

            url = response.url + str(i) + ".html"
            yield scrapy.FormRequest(url=url,callback=self.processNewsUrl)
            # break

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
        return str(req.read()).decode(encoding='gbk').encode(encoding='utf-8')





    def processNewsUrl(self,response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="pageList"]/dl').extract()
        for item in urls:
            s = Selector(text=item)
            labellist = s.xpath('//dd/p[2]/span[2]/a/text()').extract()
            url = s.xpath('//dd/h2/a/@href').extract()[0]
            labels = ""
            for i in range(1,len(labellist)):
                labels = labels + labellist[i] + " "
            labels = labels.strip()
            yield scrapy.FormRequest(url,meta={'label':labels},callback=self.processNews)
            # break

    def processNews(self,response):
        sel = Selector(response)
        pub_time = sel.xpath('//div[@class="pageContent"]/div[@class="titleInfo"]/span[1]/text()').extract()[0].split(' ')[0].replace('-','')
        pub_time = int(pub_time)
        pages = sel.xpath('//div[@id="pages"]').extract()
        pageNum = 0
        try:

            getPage = BeautifulSoup(pages[0])
            print "*******************-----------------------------------------------"
            PageBoxs = getPage.get_text().split(' ')
            pageNum = int(PageBoxs[len(PageBoxs) - 2])
        except:
            pass


        if pub_time > self.time:
            item = CrawlnewsItem()
            item['title'] = sel.xpath('//div[@class="pageContent"]/div[@class="title"]/h1/text()').extract()
            # print type(item['title'])

            if type(item['title']) == type([1]):
                item['title'] = item['title'][0]

            item['time'] = sel.xpath('//div[@class="pageContent"]/div[@class="titleInfo"]/span[1]/text()').extract()
            if type(item['time']) == type([1]):
                item['time'] = item['time'][0]

            item['kind'] = sel.xpath('//div[@class="hdbox wp"]/div[2]/div[1]/a[2]/text()').extract()

            if type(item['kind']) == type([1]):
                item['kind'] = item['kind'][0]

            item['labels'] = response.meta.get('label')

            item['secondSource'] = sel.xpath('//div[@class="pageContent"]/div[@class="titleInfo"]/span[2]/text()').extract()
            if type(item['secondSource']) == type([1]):
                try:

                    item['secondSource'] = item['secondSource'][0]
                except:
                    pass
            content = ""
            tmp = sel.xpath('//div[@class="pageContent"]/div[@id="artibody"]/p').extract()
            for i in range(0,len(tmp) - 1):
                # print tmp[i]
                print "--------------------------------------------------------------"
                # print len(tmp)
                soup = BeautifulSoup(tmp[i])
                if len(soup.get_text()) > 0:
                    content = content + soup.get_text() + " "
            for k in range(2,pageNum + 1):
                print "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
                url = str(response.url)
                url = url[0:url.rfind('.')] + "_" + str(k) + url[url.rfind('.'):len(url)]
                resp = self.getResponse(url)
                # print resp
                # time.sleep(1000)
                # print type(resp)
                # time.sleep(1000)
                select = Selector(text=resp)
                tmp1 = select.xpath('//div[@class="pageContent"]/div[@id="artibody"]/p').extract()
                for l in range(0, len(tmp1) - 1):
                    # print tmp[i]
                    print "--------------------------------------------------------------"
                    # print len(tmp)
                    soup1 = BeautifulSoup(tmp1[l])
                    print soup1.get_text()
                    if len(soup1.get_text()) > 0:
                        content = content + soup1.get_text() + " "
            item['content'] = content
            item['firstSource'] = 'kejixun'
            # print item
            # time.sleep(10000)
            yield item



