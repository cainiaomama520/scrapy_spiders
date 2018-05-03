# -*- coding: utf-8 -*-

from selenium import webdriver
from optparse import OptionParser
import csv
import pymongo
import codecs


class QqShuoshuo:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['scrapy_db']
        self.connection = self.db['QQ']
        self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()

    def get_opt(self):
        parser = OptionParser()
        parser.add_option('-p', '--path', action='store',
                          type='string', dest='path',
                          metavar='PATH', help='The storage location of the CSV file.')
        opt, args = parser.parse_args()
        return opt

    def get_qq_list(self, opt):

        qq_list = []
        with codecs.open(opt.path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                qq_list.append(row['电子邮件'].split('@')[0])

        return qq_list

    def get_info(self, qq):
        self.driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_id('login_div')
            a = True
        except:
            a = False
        if a == True:
            self.driver.switch_to.frame('login_frame')
            self.driver.find_element_by_id('switcher_plogin').click()
            self.driver.find_element_by_id('u').clear()
            self.driver.find_element_by_id('u').send_keys('1151682534')
            self.driver.find_element_by_id('p').clear()
            self.driver.find_element_by_id('p').send_keys('01259.luli')
            self.driver.find_element_by_id('login_button').click()
        self.driver.implicitly_wait(13)
        try:
            self.driver.find_element_by_id('QM_OwnerInfo_Icon')
            b = True
        except:
            b = False
        if b == True:
            self.driver.switch_to.frame('app_canvas_frame')
            contents = self.driver.find_elements_by_css_selector('.content')
            times = self.driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
            for content, time in zip(contents, times):
                data = {
                    'time': time.text,
                    'content': content.text
                }
                self.connection.insert_one(data)

if __name__ == '__main__':
    q1 = QqShuoshuo()
    opt = q1.get_opt()
    qq_list = q1.get_qq_list(opt)
    q1.get_info(qq_list)