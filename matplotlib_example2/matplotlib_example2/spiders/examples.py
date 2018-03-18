# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from matplotlib_example2.items import MatplotlibExample2Item


class ExamplesSpider(scrapy.Spider):

    name = 'examples'
    allowed_domains = ['matplotlib.org']
    start_urls = ['http://matplotlib.org/examples/index.html']

    def parse(self, response):

        le=LinkExtractor(restrict_css="div.toctree-wrapper.compound li.toctree-l2")
        links = le.extract_links(response)
        for link in links:
            yield Request(link.url,callback=self.get_source,dont_filter=True)

    def get_source(self,response):

        item = MatplotlibExample2Item()
        href = response.css("a.reference.external::attr(href)").extract_first()
        url = response.urljoin(href)
        item['file_urls'] = [url]
        yield item

