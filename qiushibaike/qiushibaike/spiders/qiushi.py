# -*- coding: utf-8 -*-
import scrapy
import re
import time
from qiushibaike.items import QiushibaikeItem


class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(i)) for i in range(1, 14)]

    def parse(self, response):
        divs = response.css('div#content > div.content-block.clearfix > div#content-left > div')
        for div in divs:
            id = div.xpath('./div[@class="author clearfix"]/.*/h2/text()').extract_first().strip()
            # id = div.css('div.author.clearfix > a:nth-child(2) > h2::text').extract_first().strip()
            sex_tag = div.xpath('./div[1]/div/@class').extract_first()
            if sex_tag == None:
                sex = 'unknow'
            else:
                sex = re.findall('[a-zA-Z]+ (.*?)Icon', sex_tag)[0]
            level = div.xpath('./div[1]/div/text()').extract_first()
            context = div.xpath('./a[1]/div[1]/span/text()').extract_first().strip()
            laugh = div.css('div.stats > span.stats-vote > i::text').extract_first().strip()
            comment = div.css('div.stats > span.stats-comments a > i::text').extract_first()
            item = QiushibaikeItem(id=id, sex=sex, level=level, context=context, laugh=laugh, comment=comment)
            yield item
