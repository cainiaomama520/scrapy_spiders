# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Item


class KugouPipeline(object):

    def open_spider(self, spider):
        self.db_uri = spider.settings.get('URI', 'mongodb://localhost:27017')
        self.db_name = spider.settings.get('DB_NAEM', 'scrapy_db')
        self.client = pymongo.MongoClient(self.db_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[spider.name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Item):
            item = dict(item)
        self.collection.insert_one(item)
        return item
