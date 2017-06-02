# -*- coding: utf-8 -*-

# Scrapy settings for testproj project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ipproj'

SPIDER_MODULES = ['ipproj.spiders']
NEWSPIDER_MODULE = 'ipproj.spiders'


IMAGES_STORE = '/home/pic_test/'

# DOWNLOAD_DELAY = 0.25
# IMAGES_THUMBS = {#缩略图的尺寸，设置这个值就会产生缩略图
#     'small': (50, 50),
#     'big': (200, 200),
# }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'testproj (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ipproj.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ipproj.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'ipproj.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

COMMANDS_MODULE = 'ipproj.commands'
ITEM_PIPELINES = {
	'ipproj.pipelines.JsonPipeline1' : 300,
    'ipproj.pipelines.JsonPipeline2' : 300,
    'ipproj.pipelines.ImageDownloadPipeline' : 80,
    #'scrapy_redis.pipelines.RedisPipeline':100, #自动加spider2：item

    'ipproj.pipelines.MongoDBFmgbPipeline': 201,
    'ipproj.pipelines.MongoDBFmsqPipeline': 203,
    'ipproj.pipelines.MongoDBXxsqPipeline': 205,
    'ipproj.pipelines.MongoDBWgsqPipeline': 207,
    'ipproj.pipelines.MongoDBBigdataPipeline': 206,
}
MONGODB_SERVER = "localhost"
# MONGODB_SERVER = "114.55.67.226"
MONGODB_PORT = 27017
MONGODB_DB = "dbpatent_bigdata"
MONGODB_COLLECTION_FMGB = "fmgb"
MONGODB_COLLECTION_FMSQ = "fmsq"
MONGODB_COLLECTION_XXSQ = "xxsq"
MONGODB_COLLECTION_WGSQ = "wgsq"
MONGODB_COLLECTION_BIGDATA = "bigdata"

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    'ipproj.middlewares.RotateUserAgentMiddleware' :400,
    'ipproj.middlewares.ProxyMiddleware': 100,
}

LOG_ENABLED = True
LOG_LEVEL = "INFO"  #  CRITICAL, ERROR, WARNING, INFO and DEBUG.
# LOG_FILE = "scrapy.log"

MEMUSAGE_REPORT = True

# DUPEFILTER_CLASS = 'ipproj.filter.custom.filters.SeenPageFilter'
DUPEFILTER_CLASS= "scrapy_redis.dupefilter.RFPDupeFilter"
'''
redis config below
'''
# Enables scheduling storing requests queue in redis.
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"   #好东西  可以保存之后跟着爬。。。。
# Schedule requests using a queue (FIFO).
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = 'localhost'#'114.55.67.226''127.0.0.1'#'114.55.67.226'
REDIS_PORT = 6379


# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

  # Ensure all spiders share same duplicates filter through redis.
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

  # Default requests serializer is pickle, but it can be changed to any module
  # with loads and dumps functions. Note that pickle is not compatible between
  # python versions.
  # Caveat: In python 3.x, the serializer must return strings keys and support
  # bytes as values. Because of this reason the json or msgpack module will not
  # work by default. In python 2.x there is no such issue and you can use
  # 'json' or 'msgpack' as serializers.
# SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"


  # Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = False

  # Schedule requests using a priority queue. (default)
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

  # Schedule requests using a priority queue. (default)
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

  # Schedule requests using a queue (FIFO).
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

  # Schedule requests using a stack (LIFO).
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

  # Max idle time to prevent the spider from being closed when distributed crawling.
  # This only works if queue class is SpiderQueue or SpiderStack,
  # and may also block the same time when your spider start at the first time (because the queue is empty).
# SCHEDULER_IDLE_BEFORE_CLOSE = 10

  # Store scraped item in redis for post-processing.
  # ITEM_PIPELINES = {
  #     'scrapy_redis.pipelines.RedisPipeline': 300
  # }

  # The item pipeline serializes and stores the items in this redis key.
REDIS_ITEMS_KEY = '%(spider)s:items'

  # The items serializer is by default ScrapyJSONEncoder. You can use any
  # importable path to a callable object.
  #REDIS_ITEMS_SERIALIZER = 'json.dumps'

  # Specify the host and port to use when connecting to Redis (optional).
  #REDIS_HOST = 'localhost'
  #REDIS_PORT = 6379

  # Specify the full Redis URL for connecting (optional).
  # If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
  #REDIS_URL = 'redis://user:pass@hostname:9001'

  # Custom redis client parameters (i.e.: socket timeout, etc.)
  #REDIS_PARAMS  = {}
  # Use custom redis client class.
  #REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

  # If True, it uses redis' ``spop`` operation. This could be useful if you
  # want to avoid duplicates in your start urls list. In this cases, urls must
  # be added via ``sadd`` command or you will get a type error from redis.
REDIS_START_URLS_AS_SET = False

  # How many start urls to fetch at once.
  #REDIS_START_URLS_BATCH_SIZE = 16

  # Default start urls key for RedisSpider and RedisCrawlSpider.
REDIS_START_URLS_KEY = '%(name)s:start_urls'
