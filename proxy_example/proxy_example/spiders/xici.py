# -*- coding: utf-8 -*-
import scrapy
import json

class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    base_url = 'http://www.xicidaili.com/nn/'


    def start_requests(self):
        for i in range(1, 11):
            yield scrapy.Request(self.base_url+str(i))

    def parse(self, response):
        trs = response.xpath('//table[@id="ip_list"]/tr[position()>1]')
        for tr in trs:
            ip = tr.css('td:nth-child(2)::text').extract_first()
            port = tr.css('td:nth-child(3)::text').extract_first()
            schema = tr.css('td:nth-child(6)::text').extract_first().lower()
            print ('proxy:', schema, ip, port)
            url = '%s://httpbin.org/ip' % schema
            proxy = '%s://%s:%s' % (schema, ip, port)
            meta = {

                'proxy': proxy,
                'dont_retry': True,
                'download_timeout': 10,
                '_proxy_schema': schema,
                '_proxy_ip': ip,
            }
            yield scrapy.Request(url, callback=self.check_available, meta=meta, dont_filter=True)

    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']
        if proxy_ip == json.loads(response.text)['origin']:
            yield {

                'proxy_schema': response.meta['_proxy_schema'],
                'proxy': response.meta['proxy'],

            }
