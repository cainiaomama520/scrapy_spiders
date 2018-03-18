# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
import browser_cookie3

class BrowserCookieMiddleware(CookiesMiddleware):

    def __int__(self, debug=False):

        super().__init__(debug)
        self.load_browser_cookie()

    def load_browser_cookie(self):

        jar = self.jars['chrome']
        chrome_cookiejar = browser_cookie3.chrome()
        for cookie in chrome_cookiejar:
            jar.set_cookie(cookie)

        jar = self.jars['firefox']
        firefox_cookiejar = browser_cookie3.firefox()
        for cookie in firefox_cookiejar:
            jar.set_cookie(cookie)

