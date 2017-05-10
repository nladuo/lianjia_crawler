# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.utils.project import get_project_settings
from items import DistrictItem, LinkItem, Item, FailedUrl


class MongoDBPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]

        self.districts = self.db["districts"]
        self.links = self.db["links"]
        self.items = self.db["items"]
        self.failed_urls = self.db["failed_urls"]

        self.districts.ensure_index('url', unique=True)
        self.links.ensure_index('url', unique=True)
        self.items.ensure_index('url', unique=True)
        self.failed_urls.ensure_index('url', unique=True)

    def get_links(self):
        return self.links.find({})

    def get_items(self, link_id):
        return self.items.find({"link_id": link_id})

    def get_failed_urls(self):
        return self.failed_urls.find({})

    def delete_failed_urls(self):
        self.failed_urls.delete_many({})

    def process_item(self, item, spider):
        if isinstance(item, DistrictItem):
            if self.districts.find({"url": item["url"]}).count() == 0:
                self.districts.insert(dict(item))
        elif isinstance(item, LinkItem):
            if self.links.find({"url": item["url"]}).count() == 0:
                self.links.insert(dict(item))
        elif isinstance(item, Item):
            if self.items.find({"url": item["url"]}).count() == 0:
                self.items.insert(dict(item))
        elif isinstance(item, FailedUrl):
            if self.failed_urls.find({"url": item["url"]}).count() == 0:
                self.failed_urls.insert(dict(item))

        return item
