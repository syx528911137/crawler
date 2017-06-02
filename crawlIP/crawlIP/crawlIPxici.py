from bs4 import BeautifulSoup
import urllib2
from ValidateIP import ValidateIP
import pymongo
import redis
import time


mongodb_host = '127.0.0.1'
mongodb_port = 27017
mongo_connection = pymongo.MongoClient(mongodb_host,mongodb_port)
conn = mongo_connection['proxyIP']
db_ips = conn['ips']
db_flag = conn['flag']

r = redis.Redis(host='localhost',port=6379)
urls = ['http://www.xicidaili.com/nn/','http://www.xicidaili.com/wn/']
validate = ValidateIP()
while True:
    for url in urls:
        # url = 'http://www.xicidaili.com/nn/' + str(page)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url=url,data=None,headers=headers)
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read(),'lxml')
        ip_list = soup.find_all('tr')
        print len(ip_list)
        for i in range(1,len(ip_list)):
            proxy = {}
            #tmp_soup = BeautifulSoup(ip_list[1],'lxml')
            content = ip_list[i].find_all('td')
            proxy['ip'] = content[1].text
            proxy['port'] = content[2].text
            proxy['kind'] = content[5].text
            flag = validate.check(proxy['ip'],proxy['port'])
            if flag:
                if r.sadd('ips',proxy['ip']):
                    db_ips.insert(proxy)
                    print "valid"
            else:
                print "---------------"
    print "waiting..."
    time.sleep(10)