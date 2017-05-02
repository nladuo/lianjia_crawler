# coding=utf8
import scrapy
from ..items import LinkItem
""" 爬取二手房所处市区的链接地址 """


class LinkSpider(scrapy.Spider):
    name = "link"
    start_urls = [
        'http://bj.lianjia.com/ershoufang/',
    ]

    def parse(self, response):
        for detail in response.css("div.position dd div")[0].css("a"):
            url = "http://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                extract_first()
            print url
            district = detail.css('a::text').extract_first()
            yield scrapy.Request(url, callback=lambda r, i=district: self.parse_detail(r, i))

    def parse_detail(self, response, district):
        for detail in response.css("div.position dd div div")[1].css("a"):
            link = LinkItem()
            link["district"] = district
            link["location"] = detail.css('a::text').extract_first()
            link["url"] = "http://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                extract_first()
            print link["url"]
            yield link
