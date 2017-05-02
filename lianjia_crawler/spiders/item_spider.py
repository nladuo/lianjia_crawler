# coding=utf8
import scrapy
from ..items import Item, FailedUrl
from ..pipelines import MongoDBPipeline
from time import time
from urllib import unquote
import json
""" 爬取二手房信息 """


class ItemSpider(scrapy.Spider):
    name = "item"
    start_urls = [
        'http://bj.lianjia.com/ershoufang/andingmen/',
    ]

    def start_requests(self):
        pipeline = MongoDBPipeline()
        for link in pipeline.get_links():
            url = link["url"]
            yield scrapy.Request(url=url, callback=lambda r, k=link["_id"], i=url: self.parse_item(r, k, i))

    def parse_item(self, response, link_id, base_url):
        print response.url
        # ip被禁了
        if response.url.startswith("http://captcha"):
            failed_url = FailedUrl()
            failed_url["url"] = unquote(response.url.split("redirect=")[1])
            failed_url["base_url"] = base_url
            failed_url["link_id"] = link_id
            yield failed_url
            return

        # 没有结果
        if response.css("div.m-noresult").extract_first() is not None:
            return

        print response.url
        for li in response.css('li.clear div.info'):
            item = Item()
            item["link_id"] = link_id
            item["url"] = li.css('div.title a::attr(href)').extract_first()
            item["title"] = li.css('div.title a::text').extract_first()
            item["xiaoqu"] = li.css('div.address a::text').extract_first()
            item["address"] = li.css('div.address div::text').extract_first()
            item["flood"] = li.css('div.flood div::text').extract_first()
            item["tag"] = li.css('div.tag span::text').extract_first()
            item["total_price"] = li.css('div.totalPrice span::text').extract_first() + \
                         li.css('div.totalPrice::text').extract_first()
            item["unit_price"] = li.css('div.unitPrice span::text').extract_first()
            item["time"] = time()

            print item["url"], item["title"], item["unit_price"]
            yield item

        # 提取下一页
        page_data = json.loads(response.css('div.contentBottom div.house-lst-page-box::attr(page-data)').
                               extract_first())
        if page_data["curPage"] < page_data["totalPage"]:
            url = base_url + "pg%d/" % (page_data["curPage"] + 1)
            print url
            yield scrapy.Request(url, callback=lambda r, k=link_id, i=base_url: self.parse_item(r, k, i))
