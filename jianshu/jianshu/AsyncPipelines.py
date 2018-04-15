# -*- coding: utf-8 -*-

from twisted.enterprise import adbapi


class MySQLAsyncPipeline:

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')

        self.dbpool = adbapi.ConnectionPool('MySQLdb', host=host, port=port, db=db,
                                       user=user, passwd=passwd, charset='utf8')

    def close_spider(self, spider):

        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        values = (
            item['data_type'],
            item['data_time'],
        )

        sql = 'INSERT INTO dongtai_tbl VALUES(%s,%s)'
        tx.execute(sql, values)