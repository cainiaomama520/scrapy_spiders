# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import time
import pymongo


class TaobaoSpider:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['scrapy_db']
        self.collection = self.db['manshort']
        self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()

    def get_info(self, url, page):
        page = page + 1
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        selector = etree.HTML(self.driver.page_source)
        infos = selector.xpath('//div[@class="item J_MouserOnverReq  "]')
        for info in infos:
            goods_name = info.xpath('string(./div[2]//div[2]/a)').strip()
            goods_price = info.xpath('string(./div[2]//div[1]//div[@class="price"])').strip()
            # goods_person = info.xpath('.//div[@class="price g_price g_price-highlight"]/div[@class="deal-cnt"]/text()').extract_first()
            shop_name = info.xpath('string(.//div[@class="shop"]//span)').strip()
            #shop_address = info.xpath('.//div[@class="shop"]/div[@class="location"]/text()').extract_first()
            commodity = {
                'good': goods_name,
                'price': goods_price,
                # 'sell': goods_person,
                'shop': shop_name,
                # 'address': shop_address
            }
            self.collection.insert_one(commodity)

        if page <= 50:
            self.next_page(url, page)
        else:
            pass

    def next_page(self, url, page):
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]').click()
        time.sleep(4)
        self.driver.get(self.driver.current_url)
        print('next_url:', self.driver.current_url)
        self.driver.implicitly_wait(10)
        self.get_info(self.driver.current_url, page)

    def main(self):
        page = 1
        url = 'http://www.taobao.com'
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('q').clear()
        self.driver.find_element_by_id('q').send_keys('男士短袖')
        self.driver.find_element_by_class_name('btn-search').click()
        print('current_url:', self.driver.current_url)
        self.get_info(self.driver.current_url, page)


if __name__ == '__main__':
    t1 = TaobaoSpider()
    t1.main()




