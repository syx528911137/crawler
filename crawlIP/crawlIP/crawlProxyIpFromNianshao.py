from bs4 import BeautifulSoup
import urllib2
from ValidateIP import ValidateIP
import pymongo
import redis
import time
from MultiProcessValidate import MultiProcessValidate


mongodb_host = '127.0.0.1'
mongodb_port = 27017
mongo_connection = pymongo.MongoClient(mongodb_host,mongodb_port)
conn = mongo_connection['proxyIP']
db_ips = conn['ips']
db_flag = conn['flag']

r = redis.Redis(host='localhost',port=6379)
urls = ['http://www.nianshao.me/?stype=1&page=1',
        'http://www.nianshao.me/?stype=1&page=2',
        'http://www.nianshao.me/?stype=2&page=1',
        'http://www.nianshao.me/?stype=2&page=2',
        ]
# validate = ValidateIP()
while True:

    for url in urls:
        ips_all = []
        # url = 'http://www.xicidaili.com/nn/' + str(page)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url=url,data=None,headers=headers)
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read(),'lxml')
        ip_list = soup.find_all('tr')

        for i in range(1,len(ip_list)):
            proxy = {}
            content = ip_list[i].find_all('td')
            proxy['ip'] = content[0].text
            proxy['port'] = content[1].text
            # proxy['kind'] = content[3].text
            # print proxy
            # time.sleep(10000)
            ips_all.append(proxy['ip'] + ":" + proxy['port'])
        validate = MultiProcessValidate(ips_all)
        validate.start()

    print "waiting..."
    time.sleep(480)