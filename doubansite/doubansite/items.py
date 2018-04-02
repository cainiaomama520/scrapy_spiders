# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DoubansiteItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    author = Field()
    publisher = Field()
    date = Field()
    price = Field()
    grade = Field()
    comm_number = Field()
