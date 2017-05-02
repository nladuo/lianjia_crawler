#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 执行爬虫, 并对对房源进行信息统计 """
import scrapydo
import time
import sys
import logging
from lianjia_crawler.pipelines import MongoDBPipeline
from lianjia_crawler.spiders.item_spider import ItemSpider
from lianjia_crawler.spiders.link_spider import LinkSpider


reload(sys)
sys.setdefaultencoding('utf8')

scrapydo.setup()


def summarize():
    pass


if __name__ == "__main__":

    logging.basicConfig(
        filename='spider.log',
        format='%(levelname)s %(asctime)s: %(message)s',
        level=logging.DEBUG
    )

    mongo = MongoDBPipeline()
    t = time.time()

    # 判断是否爬取了link
    if mongo.get_links().count() == 0:
        print "爬取地区链接...."
        scrapydo.run_spider(LinkSpider)

    # 爬取item
    while True:
        print "爬取房源中....."
        scrapydo.run_spider(ItemSpider)
        if mongo.get_failed_urls().count() == 0:
            break
        print "休息一天再爬...."
        time.sleep(24 * 3600)  # 一天之后再爬

    # 进行统计
    print "爬取结束, 耗时%d秒" % (time.time() - t)
    summarize()

    # 清空links表
    mongo.delete_items()

    print "完成!!"