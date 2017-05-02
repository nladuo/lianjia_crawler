# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.utils.project import get_project_settings
from items import LinkItem, Item, FailedUrl


class MongoDBPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.links = db["links"]
        self.items = db["items"]
        self.failed_urls = db["failed_urls"]
        self.links.ensure_index('url', unique=True)
        self.items.ensure_index('url', unique=True)
        self.failed_urls.ensure_index('url', unique=True)

    def get_links(self):
        return self.links.find({})

    def get_failed_urls(self):
        return self.failed_urls.find({})

    def delete_failed_urls(self):
        self.failed_urls.delete_many({})

    def delete_items(self):
        self.items.delete_many({})

    def process_item(self, item, spider):
        if isinstance(item, LinkItem):
            self.links.insert(dict(item))
        elif isinstance(item, Item):
            self.items.insert(dict(item))
        elif isinstance(item, FailedUrl):
            self.failed_urls.insert(dict(item))

        return item
