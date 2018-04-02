# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor




class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/annual/2017?source=navigation#{}'.format(str(i)) for i in range(1, 7)]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'images': 0, 'timeout': 10})

    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//ul[@class="g5ts0"]/li[@class="_3-jWQ"]')
        links = le.extract_links(response)
        print('links', links)
        for link in links:
            yield SplashRequest(link.url, callback=self.get_result, dont_filter=True)

    def get_result(self, response):
       info = response.css('div#content div#info').xpath('string(.)').extract_first()
       print(info)