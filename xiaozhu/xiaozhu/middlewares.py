# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import random
import codecs
import json
import pymongo
from scrapy import Item

class MyProxyMiddleware(HttpProxyMiddleware):

    ip_pools=[]
    with codecs.open(r'G:\scrapy_spiders\xiaozhu\xiaozhu\proxy.json','r','utf-8') as f:
        ips=json.load(f)
        for item in ips:
            if item['proxy_schema']=='http':
                ip_pools.append(item['proxy'])

    def process_request(self, request, spider):
        proxy=random.choice(self.ip_pools)
        print('proxy:',proxy)
        try:
            request.meta['proxy']=proxy
        except Exception as e:
            print(e)
            pass





class MongoMiddleware(object):

    def open_spider(self,spider):
        self.uri=spider.settings.get('MONGO_URI','mongodb://localhost:27017')
        self.name=spider.settings.get('MONGO_NAME','scrapy_db')
        self.client=pymongo.MongoClient(self.uri)
        self.db_name=self.client[self.name]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        if isinstance(item,Item):
            item=dict(item)

        collection=self.db_name[spider.name]
        collection.insert_one(item)
