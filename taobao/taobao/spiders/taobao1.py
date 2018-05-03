# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time



class Taobao1Spider(scrapy.Spider):
    name = 'taobao1'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']
    driver = webdriver.PhantomJS()
    driver.maximize_window()

    def start_requests(self):
        for url in self.start_urls:
            self.driver.get(url)
            self.driver.implicitly_wait(10)

    def parse(self, response):
        self.page=1
        search = self.driver.find_element_by_id('q')
        search.clear()
        search.send_keys('男士短袖')
        self.driver.find_element_by_class_name('submit icon-btn-search').click()
        print('current_url:', self.driver.current_url)
        scrapy.Request(self.driver.current_url, callback=self.get_info, dont_filter=True)

    def get_info(self, response):





