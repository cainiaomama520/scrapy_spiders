# -*- coding: utf-8 -*-
import scrapy
#from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from xiaozhu.items import XiaozhuItem


class BjxiaozhuSpider(scrapy.Spider):
    name = 'bjxiaozhu'
    allowed_domains = ['bj.xiaozhu.com']
    start_urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1, 14)]

    def parse(self, response):
        links = response.xpath('//ul[@class="pic_list clearfix"]/li/div/@detailurl').extract()
        for link in links:
            yield Request(link, callback=self.get_info, dont_filter=True)

    def get_info(self, response):

        title = response.xpath('//div[@class="pho_info"]/h4/em/text()').extract_first()
        address = response.xpath('//div[@class="pho_info"]//span/text()').extract_first()
        price = response.css('div#pricePart span::text').extract_first()
        fangdong_name = response.xpath('//div[@class="js_box clearfix"]/div[2]//a/text()').extract_first()
        sex_tag = response.xpath('//div[@class="js_box clearfix"]/div[2]//span/@class').extract_first()
        sex = self.judge_sex(sex_tag)

        item = XiaozhuItem(title=title, address=address, price=price, fangdong_name=fangdong_name, sex=sex)

        yield item
    def judge_sex(self,sex_tag):

        if sex_tag=='member_boy_ico':
            sex = '男'
        else:
            sex = '女'
        return sex


