# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    kind = scrapy.Field()
    labels = scrapy.Field()
    firstSource = scrapy.Field()
    secondSource = scrapy.Field()
    pass



class CrawlPaperItem(scrapy.Item):
    title = scrapy.Field()
    abstract = scrapy.Field()
    author = scrapy.Field()
    subjects = scrapy.Field()