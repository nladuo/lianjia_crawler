#!/usr/bin/env bash

while True:
do
    python -u run_crawler.py
    echo "run_crawler.py运行结束, 歇5天"
    sleep 120h
done
