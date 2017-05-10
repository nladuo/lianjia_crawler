# coding=utf8
import scrapy
from ..items import Item, FailedUrl
from ..pipelines import MongoDBPipeline
from time import time
import json
""" 爬取二手房信息 """


class ItemSpider(scrapy.Spider):
    name = "item"

    def start_requests(self):
        pipeline = MongoDBPipeline()
        if pipeline.get_failed_urls().count() == 0:
            # 第一次爬取, 根据link表爬取
            for link in pipeline.get_links():
                url = link["url"]
                yield scrapy.Request(url=url,
                                     dont_filter=True,
                                     callback=lambda r, k=link["_id"], m=url, i=url: self.parse_item(r, k, m, i),
                                     errback=lambda f, k=link["_id"], m=url, i=url: self.errback(f, k, m, i))
        else:
            # 读取失败的链接到内存
            failed_urls = []
            for failed_url in pipeline.get_failed_urls():
                failed_urls.append(failed_url)
            # 清空failed_urls
            pipeline.delete_failed_urls()
            # 爬取下载失败的url
            for failed_url in failed_urls:
                url = failed_url["url"]
                link_id = failed_url["link_id"]
                base_url = failed_url["base_url"]
                yield scrapy.Request(url=url,
                                     dont_filter=True,
                                     callback=lambda r, k=link_id, m=url, i=base_url: self.parse_item(r, k, m, i),
                                     errback=lambda f, k=link_id, m=url, i=base_url: self.errback(f, k, m, i))

    def parse_item(self, response, link_id, init_url, base_url):
        # ip被禁了, 或者代理出现错误
        if not response.url.startswith("http://bj.lianjia"):
            print "Anti-Spider occurred, \n\tredirect to: ", response.url, "\n\tre-adding url:", init_url
            failed_url = FailedUrl()
            failed_url["url"] = init_url
            failed_url["base_url"] = base_url
            failed_url["link_id"] = link_id
            yield failed_url
            return

        print response.url

        # 没有任何结果
        if response.css("div.m-noresult").extract_first() is not None:
            return

        print response.url

        # 保存到mongodb
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
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=lambda r, k=link_id, m=url, i=base_url: self.parse_item(r, k, m, i),
                                 errback=lambda f, k=link_id, m=url, i=base_url: self.errback(f, k, m, i))

    def errback(self, failure, link_id, init_url, base_url):
        print repr(failure)
        failed_url = FailedUrl()
        failed_url["url"] = init_url
        failed_url["base_url"] = base_url
        failed_url["link_id"] = link_id
        yield failed_url

