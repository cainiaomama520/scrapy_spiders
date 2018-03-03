# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join




class MyFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        path1 = urlparse(request.url).path
        return join(basename(dirname(path1)), basename(path1))