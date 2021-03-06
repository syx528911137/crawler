# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpprojItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    authId = scrapy.Field()
    authDate = scrapy.Field()
    appId = scrapy.Field()
    appDate = scrapy.Field()
    appOwner = scrapy.Field()
    appOwner2 = scrapy.Field()
    inventor = scrapy.Field()
    inventor2 = scrapy.Field()
    address = scrapy.Field()
    catId = scrapy.Field()
    abstract = scrapy.Field()
    downUrl = scrapy.Field()
    otherDetail = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_thumb_urls = scrapy.Field()
    downloadlink =  scrapy.Field()
    pass
