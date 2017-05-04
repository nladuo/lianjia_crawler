#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 统计测试 """
import scrapydo
import time
import sys
import logging
from lianjia_crawler.pipelines import MongoDBPipeline
import re

reload(sys)
sys.setdefaultencoding('utf8')

scrapydo.setup()


def summarize():
    for link in mongo.get_links():
        _min = 9999999  # 每平米最低价格
        _max = 0        # 每平米最高价格
        total = 0      # 每平米总价格
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
            "time": time.time(),
            "link_id": link["_id"],
            "avg": _avg,
            "min": _min,
            "max": _max
        })
        print link["district"], link["location"], "均价:", _avg, "最低:", _min, "最高:", _max


if __name__ == "__main__":
    mongo = MongoDBPipeline()
    summarize()
    # 清空links表
    mongo.delete_items()

