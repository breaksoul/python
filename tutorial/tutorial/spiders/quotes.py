# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        quotes = response.css('.quote')#先用选择器选择出包含有quote的对象并赋值
        for quote in quotes: #for 循环对每个 quote 遍历，解析每个 quote 的内容。
			item = QuoteItem()
			item['text'] = quote.css('.text::text').extract_first()#以使用 extract_first() 方法，对于 tags，要获取所有结果组成的列表，所以使用 extract() 方法。
        	item['author'] = quote.css('.author::text').extract_first()
        	item['tags'] = quote.css('.tags .tag::text').extract()#extract经常用来切片从一个对象中获得一个list#extract经常用来切片从一个对象中获得一个list
        	yield item#这一步就连接到了item


        #爬取整个网站可以继续添加代码如下
        next = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)#回调函数继续调用parse


