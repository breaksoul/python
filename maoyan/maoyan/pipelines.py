# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class MaoyanPipeline(object):
	def __init__(self):
		self.conn=pymysql.connect(host='localhost',port=3306,user='root',password='wb123456789',charset='utf8',db='maoyan')
		print('开始连接数据库')

	def process_item(self, item, spider):
		sql='insert into file(name,star,time) values(%s,%s,%s)'
		self.conn.cursor().execute(sql,(item['title'],item['star'],time['scrapy']))
		self.conn.commit


	def close_spider(self, spider):
		self.cursor.close()
		self.connect.close()
    	
    		
    	

