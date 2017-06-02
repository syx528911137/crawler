#-*-coding:UTF-8-*-
import urllib2


from scrapy.selector import Selector

class ValidateIP:
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
