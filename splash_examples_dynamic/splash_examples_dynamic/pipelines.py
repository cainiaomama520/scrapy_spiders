# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Item

class SplashExamplesDynamicPipeline(object):

    def open_spider(self,spider):
        db_uri=spider.settings.get('MONGODB_URI','mongodb://localhost:27017')
        db_name=spider.settings.get('MONGODB_NAME','scrapy_db')
        collection_name = spider.settings.get('COLLECTION_NAME', 'books')
        self.client=pymongo.MongoClient(db_uri)
        self.db=self.client[db_name]
        self.collection=self.db[collection_name]

    def close_spider(self,spider):

        self.client.close()

    def process_item(self, item, spider):

        if isinstance(item,Item):
            item=dict(item)
        self.collection.insert_one(item)
        return item
