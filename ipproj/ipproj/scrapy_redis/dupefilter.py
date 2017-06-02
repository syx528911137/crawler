#!/usr/bin/python
#-*-coding:utf-8-*-

import redis
import time
import logging
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.utils.url import canonicalize_url


class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, server, key):
        """Initialize duplication filter

        Parameters
        ----------
        server : Redis instance
        key : str
            Where to store fingerprints
        """
        logging.info( "RFPDupeFilter is start ")
        self.server = server
        self.key = key

    def __request_fingerprint(self, request):
        fp = hashlib.sha1()
        # fp.update(to_bytes(canonicalize_url(request.url)))
        logging.info("other info : " + request.body)
        fp.update(request.body or b'')
        # mm = request.url+request.meta.get('type', None)+request.body # or something like that
        logging.info( "fp is : " + fp.hexdigest())
        return fp.hexdigest()

    @classmethod
    def from_settings(cls, settings):
        logging.info("filters from_settings method")
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        # create one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """
            use sismember judge whether fp is duplicate.
        """
        logging.info("request_seen is start")
        fp = self.__request_fingerprint(request)
        if self.server.sismember(self.key,fp):
            logging.info("there is a new url" )
            return True
        self.server.sadd(self.key, fp)
        return False

    def close(self, reason):
        logging.info("filter close");
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        logging.info("filter clear redis")
        """Clears fingerprints data"""
        # self.server.delete(self.key)
