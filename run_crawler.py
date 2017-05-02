#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 执行爬虫, 并对对房源进行信息统计 """
import scrapy
from scrapy import cmdline
from lianjia_crawler.pipelines import MongoDBPipeline
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def summarize():
    pass


if __name__ == "__main__":
    mongo = MongoDBPipeline()
    t = time.time()

    # 判断是否爬取了link
    if mongo.get_links().count() == 0:
        print "爬取地区链接...."
        cmdline.execute("scrapy crawl link".split())

    # 爬取item
    while True:
        print "爬取房源中....."
        cmdline.execute("scrapy crawl item".split())
        if mongo.get_failed_urls().count() == 0:
            break
        print "休息一天再爬...."
        time.sleep(24 * 3600)  # 一天之后再爬

    # 进行统计
    print "爬取结束, 耗时%d" % (time.time() - t)
    summarize()

    # 清空links表
    mongo.delete_items()

    print "完成!!"