from bs4 import BeautifulSoup
import urllib2
from ValidateIP import ValidateIP
import pymongo
import redis
import time
import re
from MultiProcessValidate import MultiProcessValidate



mongodb_host = '127.0.0.1'
mongodb_port = 27017
mongo_connection = pymongo.MongoClient(mongodb_host,mongodb_port)
conn = mongo_connection['proxyIP']
db_ips = conn['ips']
db_flag = conn['flag']

r = redis.Redis(host='localhost',port=6379)
validate = ValidateIP()
while True:
    # for url in urls:
    ip_group = [[],[],[],[],[],[],[],[]]
    url = 'http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(url=url,data=None,headers=headers)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read(),'lxml')
    ip_list = soup.find_all('body')
    print ip_list
    ip_list = str(ip_list[0])
    print type(ip_list)
    matchObj = re.findall(r'\d*\.\d*\.\d*\.\d*:\d*', string=ip_list, flags=0)
    for i in range(0,len(matchObj)):
        index = i % 8
        ip_group[index].append(matchObj[i])
        # proxy = {}
        # tmp = ip.split(":")
        # proxy['ip'] = tmp[0]
        # proxy['host'] = tmp[1]
        # # content = ip_list[i].find_all('td')
        # # proxy['ip'] = content[1].text
        # # proxy['port'] = content[2].text
        # # proxy['kind'] = content[5].text
        # flag = validate.check(proxy['ip'],proxy['port'])
        # if flag:
        #     if r.sadd('ips',proxy['ip']):
        #         db_ips.insert(proxy)
        #         print "valid"
        # else:
        #     print "---------------"
    validate1 = MultiProcessValidate(ip_group[0])
    validate2 = MultiProcessValidate(ip_group[1])
    validate3 = MultiProcessValidate(ip_group[2])
    validate4 = MultiProcessValidate(ip_group[3])
    validate5 = MultiProcessValidate(ip_group[4])
    validate6 = MultiProcessValidate(ip_group[5])
    validate7 = MultiProcessValidate(ip_group[6])
    validate8 = MultiProcessValidate(ip_group[7])

    validate1.start()
    validate2.start()
    validate3.start()
    validate4.start()
    validate5.start()
    validate6.start()
    validate7.start()
    validate8.start()
    print "waiting..."
    time.sleep(600)