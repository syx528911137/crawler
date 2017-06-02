#-*-coding:UTF-8-*-
import urllib2
# import base64
import random
import settings
import pymongo
# from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
# from ValidateIP import ValidateIP
# import time
import redis

from scrapy.selector import Selector

class ValidateIP:

    def __init__(self):
        self.count = 0
        # self.validate = ValidateIP()
        self.mongodb_host = settings.MONGODB_HOST
        self.mongodb_port = settings.MONGODB_PORT
        self.mongo_connection = pymongo.MongoClient(self.mongodb_host, self.mongodb_port)
        self.conn = self.mongo_connection['proxyIP']
        self.db = self.conn['ips']
        self.tmp_proxy = self.conn.ips.find()
        self.r = redis.Redis(host='localhost', port=6379)
        # print "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
        # print len(self.tmp_proxy)
        self.PROXIES = []
        for ip in self.tmp_proxy:
            tmp = {}
            tmp['ip_port'] = ip['ip'] + ":" + ip['port']
            tmp['user_pass'] = ''
            print tmp
            self.PROXIES.append(tmp)


    def getValidProxyIp(self):
        self.count = self.count + 1
        if len(self.PROXIES) < 5 or self.count % 50 == 0:
            self.tmp_proxy = self.db.find()
            self.PROXIES = []
            for ip in self.tmp_proxy:
                tmp = {}
                tmp['ip_port'] = ip['ip'] + ":" + ip['port']
                tmp['user_pass'] = ''
                self.PROXIES.append(tmp)
        # print "**************************************" + len(self.PROXIES) + "***************************************"
        proxy = {}
        while True:

            proxy = random.choice(self.PROXIES)
            ip_port = proxy['ip_port'].split(':')
            ip = ip_port[0]
            port = ip_port[1]
            flag = self.check(ip, port)
            if flag:
                break
            else:
                self.PROXIES.remove(proxy)
                self.db.remove({'ip': ip})
                self.r.srem('ips', ip)
        return proxy




    def check(self,host,port):
        tmp_proxy = str(host) + ":" + str(port)
        print tmp_proxy
        url = 'http://ip.catr.cn/'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        proxy = {'http': tmp_proxy}
        headers = [('User-Agent', user_agent)]
        proxy_s = urllib2.ProxyHandler(proxies=proxy)
        opener = urllib2.build_opener(proxy_s)
        opener.addheaders = headers

        try:
            req = opener.open(url, data=None,timeout=5)
            the_page = req.read()


            sel = Selector(text=the_page)
            ip = sel.xpath('//*[@id="keyword"]/@value').extract()[0]




            if ip == host:
                return True
            else:
                return False
        except:
            return False
