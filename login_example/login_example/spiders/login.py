# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile?_next=/places/default/index']

    def parse(self, response):

        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        item = dict(zip(keys, values))
        print('item:', item)
        yield item

    # -------------登录------------------------

    login_url = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'

    def start_requests(self):

        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        # 登录的两种方式
        ''' sel = response.xpath('.//div[@style]/input')
        print ('sel', sel)
        fd1 = dict(zip(sel.xpath('./@name').extract(), sel.xpath('./@value').extract()))
        fd1['email'] = '18611378520@163.com'
        fd1['password'] = '!QAZ2wsx'
        print('fd1:', fd1)
        yield FormRequest(self.login_url, formdata=fd1, callback=self.parse_login, dont_filter=True)
        '''

        fd2 = {'email': '18611378520@163.com', 'password': '!QAZ2wsx'}
        yield FormRequest.from_response(response, formdata=fd2, callback=self.parse_login)

    def parse_login(self, response):

        # print(response.text)
        if 'luli' in response.text:
            yield from super().start_requests()


