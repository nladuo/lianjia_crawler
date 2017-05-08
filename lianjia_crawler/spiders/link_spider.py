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
        if not response.url.startswith("http://bj.lianjia"):
            yield scrapy.Request(self.start_urls[0], callback=self.parse)

        for detail in response.css("div.position dd div")[0].css("a"):
            url = "http://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                extract_first()
            print url
            district = detail.css('a::text').extract_first()
            yield scrapy.Request(url, callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                 errback=lambda r, k=url: self.errback(r, k))

    def parse_detail(self, response, url, district):
        if not response.url.startswith("http://bj.lianjia"):
            print "response error occurred, status_code:", response.status, " url:", response.url
            yield scrapy.Request(url, callback=lambda r, k=url, i=district: self.parse_detail(r, k, i))

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

    def errback(self, failure, url):
        print repr(failure), "\n\turl:", url



