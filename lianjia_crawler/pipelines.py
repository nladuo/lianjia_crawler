# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from items import LinkItem, Item


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.links = db["links"]
        self.items = db["items"]
        self.links.ensure_index('url', unique=True)
        self.items.ensure_index('url', unique=True)

    def get_links(self):
        return self.links.find({})

    def process_item(self, item, spider):
        if isinstance(item, LinkItem):
            self.links.insert(dict(item))
        elif isinstance(item, Item):
            self.items.insert(dict(item))

        return item
