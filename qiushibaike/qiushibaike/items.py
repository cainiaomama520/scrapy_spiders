# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item

class QiushibaikeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    level = Field()
    sex = Field()
    context = Field()
    laugh = Field()
    comment = Field()
