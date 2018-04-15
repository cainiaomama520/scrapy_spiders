# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb



class MySQLPipelines:

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')

        self.db_conn = MySQLdb.Connect(host=host, port=port, db=db,
                                       user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['data_type'],
            item['data_time'],
        )

        sql = 'INSERT INTO dongtai_tbl VALUES(%s,%s)'
        self.db_cur.execute(sql, values)