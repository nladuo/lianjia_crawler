# coding=utf8
import scrapy
from ..items import LinkItem, DistrictItem
import json
""" 爬取二手房所处市区的链接地址 """


class LinkSpider(scrapy.Spider):
    name = "link"
    s_urls = [
        'https://bj.lianjia.com/ershoufang/',
    ]

    def start_requests(self):
        yield scrapy.Request(self.s_urls[0],
                             dont_filter=True,
                             callback=self.parse,
                             errback=lambda r, k="", i="": self.errback(r, k, i))

    def parse(self, response):
        if not response.url.startswith("https://bj.lianjia"):
            yield scrapy.Request(self.s_urls[0],
                                 dont_filter=True,
                                 callback=self.parse,
                                 errback=lambda r, k="", i="": self.errback(r, k, i))

        for detail in response.css("div.position dd div")[0].css("a"):
            url = "https://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                extract_first()
            print url
            district = detail.css('a::text').extract_first()
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                 errback=lambda r, k=url, i=district: self.errback(r, k, i))

    def parse_detail(self, response, url, district):
        if not response.url.startswith("https://bj.lianjia"):
            print "Anti-Spider occurred, \n\tredirect to: ", response.url, "\n\tre-adding url:", url
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                 errback=lambda r, k=url, i=district: self.errback(r, k, i))

        district_item = DistrictItem()
        district_item["url"] = response.url
        district_item["name"] = district
        locations = []
        for detail in response.css("div.position dd div div")[1].css("a"):
            link = LinkItem()
            link["district"] = district
            link["location"] = detail.css('a::text').extract_first()
            link["url"] = "https://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                extract_first()
            locations.append(link["location"])
            print link["url"]
            yield link
        district_item["locations"] = json.dumps(locations)
        yield district_item

    def errback(self, failure, url, district):
        """ 出现失败重新添加到爬虫队列 """
        print repr(failure)
        if url == "":
            print "\tre-adding url:", self.s_urls[0]
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                 errback=lambda r, k=url, i=district: self.errback(r, k, i))
        else:
            print "\tre-adding url:", url
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                 errback=lambda r, k=url, i=district: self.errback(r, k, i))



