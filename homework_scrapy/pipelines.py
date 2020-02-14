# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from pymysql import cursors


class HomeworkScrapyPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '5642818',
            'database': 'wxjc',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)

    def process_item(self, item, spider):
        # 将插入item的操作交给runInteraction进行异步调用，如果以直接调用函数作为参数，则是同步的操作
        try:
            # 会返回一个defer对象，可用他进行错误处理
            self.dbpool.runInteraction(self.insert, item)
        except:
            print("*"*30)
            print("写入error")

    def insert(self,cursor,item):
        sql = "insert into appjc values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        value = (item['title'], item['word1'], item['word2'], item['word3'], item['author']
                 , item['author_img'], item['time'], item['viewnum'], item['introduction'], item['content'])
        cursor.execute(sql,value)
        return item

    def close_spider(self,spider):
        self.dbpool.close()
