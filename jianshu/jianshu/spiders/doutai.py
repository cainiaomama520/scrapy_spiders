# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from jianshu.items import JianshuItem


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['www.jianshu.com']
    base_url = 'https://www.jianshu.com/users/9104ebf5e177/timeline'
    page = 2

    def start_requests(self):

        yield Request(self.base_url, dont_filter=True)

    def parse(self, response):

        data_types = response.xpath('//li//div[@class="author"]//span/@data-type').extract()
        data_times = response.xpath('//li//div[@class="author"]//span/@data-datetime').extract()
        item = JianshuItem()
        for data_type, data_time in zip(data_types, data_times):
            item['data_type'] = data_type
            item['data_time'] = data_time
            yield item

        id = response.css('li:nth-last-child(1)::attr(id)').extract_first()
        if id is not None:
            max_id = int(id.split('-')[1]) - 1
            next_page = self.base_url + '?max_id=%s&page=%s' % (max_id, self.page)
            yield Request(next_page, callback=self.parse, dont_filter=True)
            self.page = self.page + 1


