#-*-coding:UTF-8-*-
import scrapy
from scrapy.selector import Selector
from crawlnews.items import CrawlnewsItem
import time

class SpiderSina(scrapy.Spider):
    name = "crawlsina"
    allowed_domains = ["sina.com.cn"]
    startURL = "http://roll.tech.sina.com.cn/s/channel.php?ch=05#col=30&spec=&type=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=1"
    pageNumber = 0












    def start_requests(self):
        # print "start_requests"
        # return [scrapy.FormRequest(self.startURL,callback=self.processPageInfo)]
        self.pageNumber = 32
        for i in xrange(1, self.pageNumber + 1):
            print "processPageInfo"
            url = "http://roll.tech.sina.com.cn/s/channel.php?ch=05#col=30&spec=&type=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=" + str(i)
            if i == 2:
                break
            yield scrapy.FormRequest(url=url, callback=self.processNewsUrls)



    def processPageInfo(self,response):
        sel = Selector(response)
        page = sel.xpath("//div[@class='pagebox']/span[14]/a").extract()
        # print str(page)
        # time.sleep(10)
        # self.pageNumber = float(str(page))
        self.pageNumber = 32
        for i in xrange(1,self.pageNumber + 1):
            print "processPageInfo"
            url = "http://roll.tech.sina.com.cn/s/channel.php?ch=05#col=30&spec=&type=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=" + str(i)
            if i == 2:
                break
            yield scrapy.FormRequest(url=url,callback=self.processNewsUrls)



    def processNewsUrls(self,response):
        sel = Selector(response)
        # with f as op
        newsURLlists = sel.xpath('//*[@id="d_list"]/ul//*[@id="d_list"]/ul').extract()
        print len(newsURLlists)
        time.sleep(100)
        for i in range(0,len(newsURLlists)):
            if i == 1:
                break
            print "processNews"
            yield scrapy.FormRequest(url=newsURLlists[i],callback=self.processNews)


    def processNews(self,response):
        sel = Selector(response)
        item = CrawlnewsItem()
        item['title'] = sel.xpath('//*[@id="main_title"]/text()').extract()
        item['time'] = sel.xpath('//*[@id="page-tools"]/span/span[1]/text()').extract()
        newlist = sel.xpath('//*[@id="artibody"]/p/text()').extract()
        news = ""
        for i in range(0,len(newlist)):
            news = news + newlist[i] + " "
            # print news
        news = news.strip()
        item['content'] = news
        item['kind'] = "tech"
        labs = sel.xpath('//*[@id="wrapOuter"]/div[2]/div[4]/p/a/text()').extract()
        label = ""
        for j in range(0,len(labs)):
            label = label + labs[j] + " "
        label = label.strip()

        item['labels'] = label
        print "processNews*************************************************************************"
        yield item



