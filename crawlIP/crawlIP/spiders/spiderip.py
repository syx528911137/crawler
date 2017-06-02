#-*-coding:UTF-8-*-
import scrapy

from scrapy.selector import Selector
from crawlIP.items import CrawlipItem
import time

class SpiderSina(scrapy.Spider):
    name = "dailiip"
    allowed_domains = ["com"]
    start_urls_kuaidaili = ["http://www.kuaidaili.com/free/inha/1/",
                            "http://www.kuaidaili.com/free/inha/2/",
                            "http://www.kuaidaili.com/free/inha/3/",
                            "http://www.kuaidaili.com/free/inha/4/",
                            "http://www.kuaidaili.com/free/inha/5/",
                            "http://www.kuaidaili.com/free/inha/6/",
                            "http://www.kuaidaili.com/free/inha/7/",
                            "http://www.kuaidaili.com/free/inha/8/",
                            "http://www.kuaidaili.com/free/inha/9/",
                            "http://www.kuaidaili.com/free/inha/10/"
                            ]
    start_urls_84ip = ["http://ip84.com/gn/1",
                       "http://ip84.com/gn/2",
                       "http://ip84.com/gn/3",
                       "http://ip84.com/gn/4",
                       "http://ip84.com/gn/5",
                       "http://ip84.com/gn/6",
                       "http://ip84.com/gn/7",
                       "http://ip84.com/gn/8",
                       "http://ip84.com/gn/9",
                       "http://ip84.com/gn/10",
                       ]
    start_urls_xici = ['http://www.xicidaili.com/nn/']
    def start_requests(self):
        print "*******************************start request************************************"
        for i in range(0,1):
            url = self.start_urls_kuaidaili[i]
            # yield scrapy.FormRequest(url=url,meta={"webName":"kuaidaili"},dont_filter=True, callback=self.processIPKuaidaiki)
        # for j in range(0,len(self.start_urls_84ip)):
        #     url = self.start_urls_84ip[j]
        #     print url
        #     yield scrapy.FormRequest(url=url,meta={"webName":"84ip"},dont_filter=True,callback=self.processIP84ip)
        for k in range(0,len(self.start_urls_xici)):
            url = self.start_urls_xici[k]
            yield scrapy.FormRequest(url=url,meta={'webName':'xici'},dont_filter=True,callback=self.processXici)


    # def processPageInfo(self,response):
    #     sel = Selector(response)
    #     page = sel.xpath("//div[@class='pagebox']/span[14]/a").extract()
    #     # print str(page)
    #     # time.sleep(10)
    #     # self.pageNumber = float(str(page))
    #     self.pageNumber = 32
    #     for i in xrange(1,self.pageNumber + 1):
    #         print "processPageInfo"
    #         url = "http://roll.tech.sina.com.cn/s/channel.php?ch=05#col=30&spec=&type=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=" + str(i)
    #         if i == 2:
    #             break
    #         yield scrapy.FormRequest(url=url,callback=self.processNewsUrls)



    def processIPKuaidaiki(self,response):
        print "************************************processIPKuaidaili**************************************"
        sel = Selector(response)
        ips = sel.xpath('//div[@id="list"]/table/tbody/tr').extract()
        # print ips
        # time.sleep(100)
        print len(ips)
        print "-----------------------------------------------------------------------------------"
        for i in range(0,len(ips)):
            item = CrawlipItem()
            # print ips[i]
            tmp = Selector(text=ips[i])
            content = tmp.xpath('//td/text()').extract()
            item['host'] = content[0]
            item['port'] = content[1]
            item['kind'] = content[3]
            yield item



    def processIP84ip(self,response):
        print "********************************process84ip*******************************************"
        sel = Selector(response)
        ips = sel.xpath('//table[@class="list"]/tr').extract()
        print len(ips)
        for i in range(1,len(ips)):
            item = CrawlipItem()
            tmp = Selector(text=ips[i])
            content = tmp.xpath('//td/text()').extract()
            item['host'] = content[0]
            item['port'] = content[1]
            item['kind'] = content[4]
            yield item


    def processXici(self,response):
        print "************************xici***************************************"