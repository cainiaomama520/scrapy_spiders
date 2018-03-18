# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request



class CookiesLoginSpider(scrapy.Spider):

    name = 'cookies_login'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/settings/profile']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, meta={'cookiejar': 'chrome'})

    def parse(self, response):
        name = response.xpath('//div[@id="rename-section"]/span/text()').extract_first()
        personal_domain = response.xpath('string(//div[@id="js-url-preview"])').extract_first()
        yield {
            'name': name,
            'personal_domain': personal_domain, }