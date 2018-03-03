# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from matplotlib_examples.items import MatplotlibExamplesItem



class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotlib.org']
    start_urls = ['http://matplotlib.org/examples/index.html']

    def parse(self, response):

        le=LinkExtractor(restrict_css='div.toctree-wrapper.compound li.toctree-l2')
        links=le.extract_links(response)
        print ('links:',len(links))
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_example)

    def parse_example(self, response):

        href=response.css('a.reference.external::attr(href)').extract_first()
        url=response.urljoin(href)
        item=MatplotlibExamplesItem()
        item['file_urls']=[url]

        yield item



