# -*- coding: utf-8 -*-
import scrapy
from lxml import etree


class MaoyanspiderSpider(scrapy.Spider):
	name = 'maoyanspider'
	allowed_domains = ['www.maoyan.com']
	offset=0
	url = 'https://maoyan.com/board/4?'#每页递增10
	start_urls=url+str(offset)

	def parse(self, response):
		res=etree.HTML(response.text)

		item['title']=res.xpath(r'//*[@id="app"]/div/div/div[1]/dl//dd/div/div/div[1]/p[1]/a/text()')
		item['star']=res.xpath(r'//*[@id="app"]/div/div/div[1]/dl//dd/div/div/div[1]/p[2]/text()')
		time['scrapy']=res.xpath(r'//*[@id="app"]/div/div/div[1]/dl//dd/div/div/div[1]/p[3]/text()')
		yield  item

		count=0
		if self.offset<20:
			self.offset+=10
			
			count+=1
			print('获取到数据',count)
			yield scrapy.Request(self.url + str(self.offset),callback=self.parse)
