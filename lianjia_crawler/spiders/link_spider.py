# coding=utf8
import scrapy
from ..items import LinkItem, DistrictItem
import json
""" 爬取二手房所处市区的链接地址 """


class LinkSpider(scrapy.Spider):
    name = "link"
    s_urls = [
        'http://bj.lianjia.com/ershoufang/',
    ]

    def start_requests(self):
        yield scrapy.Request(self.s_urls[0],
                             dont_filter=True,
                             callback=self.parse,
                             errback=lambda r, k="", i="": self.errback(r, k, i))

    def parse(self, response):
        if not response.url.startswith("http://bj.lianjia"):
            yield scrapy.Request(self.s_urls[0],
                                 dont_filter=True,
                                 callback=self.parse,
                                 errback=lambda r, k="", i="": self.errback(r, k, i))

        try:
            for detail in response.css("div.position dd div")[0].css("a"):
                url = "http://bj.lianjia.com/%s" % detail.css('a::attr(href)').\
                    extract_first()
                print url
                district = detail.css('a::text').extract_first()
                yield scrapy.Request(url,
                                     dont_filter=True,
                                     callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                     errback=lambda r, k=url, i=district: self.errback(r, k, i))
        except:
            yield scrapy.Request(self.s_urls[0],
                                 dont_filter=True,
                                 callback=self.parse,
                                 errback=lambda r, k="", i="": self.errback(r, k, i))

    def parse_detail(self, response, url, district):
        if not response.url.startswith("http://bj.lianjia"):
            print "Anti-Spider occurred, re-adding url:", response.url
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                 errback=lambda r, k=url, i=district: self.errback(r, k, i))

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
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=lambda r, k=url, i=district: self.parse_detail(r, k, i),
                                 errback=lambda r, k=url, i=district: self.errback(r, k, i))

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



