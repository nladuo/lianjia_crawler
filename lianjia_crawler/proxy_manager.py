# -*- coding: utf-8 -*-
import requests
import json


class ProxyManager:

    instance = None

    def __init__(self):
        resp = requests.get("http://127.0.0.1:8000/select?name=lianjia")
        self.proxies = json.loads(resp.content)
        self.pointer = 0

    @staticmethod
    def get_instance():
        if ProxyManager.instance is None:
            ProxyManager.instance = ProxyManager()

        return ProxyManager.instance

    def get_proxy(self):
        if len(self.proxies) == 0:
            return None
        proxy = self.proxies[self.pointer]
        self.pointer += 1
        if self.pointer == len(self.proxies):
            resp = requests.get("http://127.0.0.1:8000/select?name=lianjia")
            self.proxies = json.loads(resp.content)
            self.pointer = 0
        return proxy
