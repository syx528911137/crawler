#-*-coding:UTF-8-*-
# import urllib
# import urllib2
# url = 'http://www.someserver.com/cgi-bin/register.cgi'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息
# values = {'name' : 'Michael Foord',
#           'location' : 'Northampton',
#           'language' : 'Python' }
# headers = { 'User-Agent' : user_agent }
# data = urllib.urlencode(values)
# req = urllib2.Request(url, data, headers)
# response = urllib2.urlopen(req)
# the_page = response.read()
# # print the_page
# import urllib
import urllib2
# from ValidateIP import ValidateIP
# tmp = ValidateIP()
# result = tmp.check('123.232.211.18','8888')
# print result
# url = 'http://ip.catr.cn/'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# proxy = {'http':'112.81.100.102:8888'}
# headers = [('User-Agent', user_agent)]
# proxy_s = urllib2.ProxyHandler(proxies=proxy)
# opener = urllib2.build_opener(proxy_s)
# opener.addheaders = headers
# #
# # values = {'name': 'Michael Foord',
# #           'location': 'pythontab',
# #           'language': 'Python'}
#
# # data = urllib.urlencode(values)
# req = opener.open(url,data=None)
# the_page = req.read()
#
#
#
#
#
#
#
#
#
#
#
#
#
# print the_page

#
# import datetime
# print type(datetime.datetime.today().year)
# req = urllib2.urlopen("http://www.kejixun.com/article/161010/232714_2.shtml")
# req = req.read().decode(encoding='gbk').encode(encoding='utf-8')
# print req
a = ['sssss']
print type(a[0]) == type([1])



for i in range(2,1):
    print "sss"




