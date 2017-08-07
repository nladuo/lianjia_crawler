#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 执行爬虫, 并对对房源进行信息统计 """
import scrapydo
import time
import sys
import logging
import re
import json
import requests
from lianjia_crawler.pipelines import MongoDBPipeline
from lianjia_crawler.spiders.item_spider import ItemSpider
from lianjia_crawler.spiders.link_spider import LinkSpider


reload(sys)
sys.setdefaultencoding('utf8')

scrapydo.setup()


def check_ip_num():
    """ 检查当前存在的可用代理ip数目 """
    resp = requests.get("http://127.0.0.1:8000/select?name=lianjia")
    count = len(json.loads(resp.content))
    print "当前可用ip数目:", count
    return count


def summarize():
    t0 = time.time()

    for link in mongo.get_links():
        _min = 9999999  # 每平米最低价格
        _max = 0        # 每平米最高价格
        total = 0       # 每平米总价格
        items = mongo.items.find({"link_id": link["_id"]})
        if items.count() == 0:
            continue
        for item in items:
            unit_price = int(re.sub("\D", "", item["unit_price"]))
            if _min > unit_price:
                _min = unit_price
            if _max < unit_price:
                _max = unit_price
            total += unit_price
        _avg = total / items.count()

        mongo.db["sum"].insert({
            "time": t0,
            "location": link["location"],
            "avg": _avg,
            "min": _min,
            "max": _max,
            "house_num": items.count()  # 爬取到的房子的个数
        })
        print link["district"], link["location"], "均价:", _avg, "最低:", _min, \
            "最高:", _max, "房源个数:", items.count()


if __name__ == "__main__":
    logging.basicConfig(
        filename='spider.log',
        format='%(levelname)s %(asctime)s: %(message)s',
        level=logging.DEBUG
    )
    print "开始连接mongodb....."
    mongo = MongoDBPipeline()
    t = time.time()

    # 1、清空items表和link表
    print "开始清空items和links表....."
    mongo.db["items"].delete_many({})
    mongo.db["links"].delete_many({})

    # 2、爬取链接，并更新district
    print "开始爬取区域链接....."
    scrapydo.run_spider(LinkSpider)

    # 3、爬取item
    while True:
        if check_ip_num() < 25:
            print "ip数不足25, 休息10分钟...."
            time.sleep(600)
            continue
        print "爬取房源中....."
        scrapydo.run_spider(ItemSpider)
        if mongo.get_failed_urls().count() == 0:
            break
        print "开始再次爬取房源...."

    print "爬取结束, 耗时%d秒" % (time.time() - t)

    # 4、根据location的名字进行统计
    print "开始统计..."
    summarize()

    print "统计完成!!"
