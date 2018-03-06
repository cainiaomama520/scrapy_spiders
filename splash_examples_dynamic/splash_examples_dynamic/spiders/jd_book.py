# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
from splash_examples_dynamic.items import SplashExamplesDynamicItem


lua_script='''   
    function main(splash)
        splash:go(splash.args.url)
        splash:wait(2)
        splash:runjs("document.getByElementsByClassName('page')[0].scrollIntoView(true)")
        splash:wait(2)
        return splash:html()
    end
'''




class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    base_url='https://search.jd.com/Search?keyword=python&enc=utf-8&wq=python'

    def start_requests(self):
        yield Request(self.base_url,callback=self.parse_urls,dont_filter=True)

    def parse_urls(self,response):

        total=int(response.css('span#J_resCount::text').re_first('([0-9]+)\+'))
        if total % 60 == 0:
            pageNum=total // 60
        else:
            pageNum=total // 60 + 1
        for i in range(pageNum):
            url='%s&page=%s' % (self.base_url,2*i+1)
            yield SplashRequest(url,endpoint='execute',args={'lua_source':lua_script},cache_args=['lua_source'])




    def parse(self, response):
        item = SplashExamplesDynamicItem()
        for sel in response.css('ul.gl-warp.clearfix > li.gl-item'):

            item['price']=sel.css('div.p-price i::text').extract_first()
            item['name']=sel.css('div.p-name').xpath('string(.//em)').extract_first()
            yield item
