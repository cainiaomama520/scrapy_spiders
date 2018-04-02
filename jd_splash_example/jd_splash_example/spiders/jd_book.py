# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy import Request
import re
from jd_splash_example.items import JdSplashExampleItem

lua_script = '''
    function main(splash)
      splash:go(splash.args.url)
      splash:wait(2)
      splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
      splash:wait(2) 
      return splash:html()
    end 
'''


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['serch.jd.com']
    base_url = "https://search.jd.com/Search?keyword=python&enc=utf-8"

    def start_requests(self):
        yield Request(self.base_url, callback=self.parse_pages, dont_filter=True)

    def parse_pages(self, response):
        num = response.css("div.f-result-sum > span.num::text").extract_first()
        book_num = int(re.findall('(.*?)\+', num)[0])
        page_num = book_num // 60
        if book_num % 60:
            page_num += 1
        else:
            page_num += 0
        for i in range(page_num):
            url = self.base_url + '&page=' + str(i * 2 + 1)
            yield SplashRequest(url, endpoint='execute', args={'lua_source': lua_script}, cache_args=['lua_source'])

    def parse(self, response):
        lis = response.css('li.gl-item')
        for li in lis:
            item = JdSplashExampleItem()
            name = li.xpath('string(.//div[@class="p-name"]//em)').extract_first()
            price = li.xpath('string(.//div[@class="p-price"]/strong)').extract_first()
            item['name'] = name
            item['price'] = price
            yield item
