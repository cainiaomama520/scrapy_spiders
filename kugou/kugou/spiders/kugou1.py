# -*- coding: utf-8 -*-
import scrapy
from kugou.items import KugouItem



class Kugou1Spider(scrapy.Spider):
    name = 'kugou1'
    allowed_domains = ['www.kugou.com']
    start_urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(str(i)) for i in range(1, 24)]

    def parse(self, response):
        lis = response.css('div.pc_temp_songlist > ul > li')
        for li in lis:
            rank = li.css('span.pc_temp_num > strong::text').extract_first()
            singer_song = li.xpath('.//a[@class="pc_temp_songname"]/text()').extract_first()
            singer = singer_song.split('-')[0]
            song = singer_song.split('-')[1]
            time = li.xpath('.//span[@class="pc_temp_time"]/text()').extract_first().strip()
            item = KugouItem(rank=rank, singer=singer, song=song, time=time)
            yield item
