import threading
from ValidateIP import ValidateIP
import redis
import pymongo


class MultiProcessValidate(threading.Thread):
    def __init__(self,ips):
        threading.Thread.__init__(self)
        self.ips = ips
        self.validate = ValidateIP()
        self.r = redis.Redis(host='localhost',port=6379)
        self.mongodb_host = '127.0.0.1'
        self.mongodb_port = 27017
        self.mongo_connection = pymongo.MongoClient(self.mongodb_host, self.mongodb_port)
        self.conn = self.mongo_connection['proxyIP']
        self.db_ips = self.conn['ips']
        # self.db_flag = self.conn['flag']

    def run(self):
        for ip in self.ips:
            print "---------------" + ip + "-----------------------"
            proxy = {}
            tmp = ip.split(":")
            proxy['ip'] = tmp[0]
            proxy['port'] = tmp[1]
            flag = self.validate.check(proxy['ip'], proxy['port'])
            # flag = self.validate.check(proxy['ip'], proxy['port'])
            if flag:
                if self.r.sadd('ips', proxy['ip']):
                    self.db_ips.insert(proxy)
                    print "valid"
            else:
                print "---------------"