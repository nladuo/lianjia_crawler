# coding=utf8
import scrapy
""" 爬取二手房所处市区的链接地址 """


class LinkSpider(scrapy.Spider):
    name = "link"
    start_urls = [
        'http://bj.lianjia.com/ershoufang/',
    ]

    def parse(self, response):
        for detail in response.css("div.position dd div")[0].css("a"):
            url = "http://bj.lianjia.com/%s" % detail.css('a::attr(href)').extract_first()
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        district = response.css("div.position dd div a.selected::text").extract_first()
        print district
        for detail in response.css("div.position dd div div")[1].css("a"):
            print "\t", detail.css('a::text').extract_first(), detail.css('a::attr(href)').extract_first()
