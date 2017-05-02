# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkItem(scrapy.Item):
    url = scrapy.Field()
    district = scrapy.Field()
    location = scrapy.Field()


class Item(scrapy.Item):
    link_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    xiaoqu = scrapy.Field()
    address = scrapy.Field()
    flood = scrapy.Field()
    tag = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    time = scrapy.Field()


class FailedUrl(scrapy.Item):
    url = scrapy.Field()
