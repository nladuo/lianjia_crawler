# coding=utf8
import scrapy
from ..items import LinkItem, DistrictItem
import json
""" 爬取二手房所处市区的链接地址 """


class LinkSpider(scrapy.Spider):
    name = "link"
    start_urls = [
        'http://bj.lianjia.com/ershoufang/',
    ]

    def parse(self, response):
        try:
            for detail in response.css("div.position dd div")[0].css("a"):
                url = "http://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                    extract_first()
                print url
                district = detail.css('a::text').extract_first()
                yield scrapy.Request(url, callback=lambda r, k=url, i=district: self.parse_detail(r, k, i))
        except:
            # 出错重新爬
            yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse_detail(self, response, url, district):
        try:
            district_item = DistrictItem()
            district_item["url"] = response.url
            district_item["name"] = district
            locations = []
            for detail in response.css("div.position dd div div")[1].css("a"):
                link = LinkItem()
                link["district"] = district
                link["location"] = detail.css('a::text').extract_first()
                link["url"] = "http://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                    extract_first()
                locations.append(link["location"])
                print link["url"]
                yield link
            district_item["locations"] = json.dumps(locations)
            yield district_item
        except:
            # 出错重新爬
            yield scrapy.Request(url, callback=lambda r, k=url, i=district: self.parse_detail(r, k, i))
