#!/usr/bin/python
# -*-coding:utf-8-*-
import base64
import random
import settings
import pymongo
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from ValidateIP import ValidateIP
import time
import redis

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            print ua, '-----------------yyyyyyyyyyyyyyyyyyyyyyyyy'
            request.headers.setdefault('User-Agent', ua)

            # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape

    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

class ProxyMiddleware(object):
    def __init__(self):
        # self.count = 0
        self.validate = ValidateIP()
        # self.mongodb_host = settings.MONGODB_HOST
        # self.mongodb_port = settings.MONGODB_PORT
        # self.mongo_connection = pymongo.MongoClient(self.mongodb_host, self.mongodb_port)
        # self.conn = self.mongo_connection['proxyIP']
        # self.db = self.conn['ips']
        # self.tmp_proxy = self.conn.ips.find()
        # self.r = redis.Redis(host='localhost',port=6379)
        # print "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
        # # print len(self.tmp_proxy)
        # self.PROXIES = []
        # for ip in self.tmp_proxy:
        #     tmp = {}
        #     tmp['ip_port'] = ip['ip'] + ":" + ip['port']
        #     tmp['user_pass'] = ''
        #     print tmp
        #     self.PROXIES.append(tmp)






    def process_request(self, request, spider):
        # self.count = self.count + 1
        # if len(self.PROXIES) < 5 or self.count % 50 == 0:
        #     self.tmp_proxy = self.db.find()
        #     self.PROXIES = []
        #     for ip in self.tmp_proxy:
        #         tmp = {}
        #         tmp['ip_port'] = ip['ip'] + ":" + ip['port']
        #         tmp['user_pass'] = ''
        #         self.PROXIES.append(tmp)
        # # print "**************************************" + len(self.PROXIES) + "***************************************"
        # while True:
        #
        #     proxy = random.choice(self.PROXIES)
        #     ip_port = proxy['ip_port'].split(':')
        #     ip = ip_port[0]
        #     port = ip_port[1]
        #     flag = self.validate.check(ip,port)
        #     if flag:
        #         break
        #     else:
        #         self.PROXIES.remove(proxy)
        #         self.db.remove({'ip':ip})
        #         self.r.srem('ips',ip)
        proxy = self.validate.getValidProxyIp()
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']