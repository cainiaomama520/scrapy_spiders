# -*- coding: utf-8 -*-
import scrapy
from pexels.items import PexelsItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['www.pexels.com']
    start_urls = ['https://www.pexels.com/search/book/?page={}'.format(str(i)) for i in range(1, 20)]

    def parse(self, response):
        image_srcs = response.xpath('//img/@src').extract()
        item = PexelsItem()
        item['image_urls'] = image_srcs[:-2]
        yield item
