import time
import connection

from scrapy.dupefilter import BaseDupeFilter
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
        self.server = server
        self.key = key

    def __request_fingerprint(self, request):
        fp = hashlib.sha1()
        fp.update(to_bytes(canonicalize_url(request.url)))
        fp.update(request.body or b'')
        # mm = request.url+request.meta.get('type', None)+request.body # or something like that
        logging.info( 'fp is : ' + fp.hexdigest())
        return fp.hexdigest()

    @classmethod
    def from_settings(cls, settings):
        server = connection.from_settings(settings)
        # create one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        added = self.server.sadd(self.key, fp)
        return not added

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.server.delete(self.key)


    

    

    """Redis-based request duplication filter"""

    # def __init__(self, server, key):
    #     """Initialize duplication filter
    #
    #     Parameters
    #     ----------
    #     server : Redis instance
    #     key : str
    #         Where to store fingerprints
    #     """
    #     self.server = server
    #     self.key = key
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     host = settings.get('REDIS_HOST', 'localhost')
    #     port = settings.get('REDIS_PORT', 6379)
    #     server = redis.Redis(host, port)
    #     # create one-time key. needed to support to use this
    #     # class as standalone dupefilter with scrapy's default scheduler
    #     # if scrapy passes spider on open() method this wouldn't be needed
    #     key = "dupefilter:%s" % int(time.time())
    #     print "key is : " + key
    #     return cls(server, key)
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls.from_settings(crawler.settings)
    #
    # def close(self, reason):
    #     """Delete data on close. Called by scrapy's scheduler"""
    #     self.clear()
    #
    # def clear(self):
    #     """Clears fingerprints data"""
    #     self.server.delete(self.key)