import requests
from lxml import etree
import json
class Guba(object):
	def __init__(self):
                
		self.url='http://guba.eastmoney.com/default,99_%s.html'
		self.headers=headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36','Cookie':'qgqp_b_id=c25d52f59be7257fa46897238d44eb58; _adsame_fullscreen_18009=1; st_si=70528332362087; st_pvi=12650593374741; st_sp=2020-05-03%2013%3A15%3A46; st_inirUrl=https%3A%2F%2Fwww.so.com%2Flink; st_sn=5; st_psi=20200503132040779-117001301773-4896786884; st_asi=20200503131650179-117001301773-7085529848-gb_xgbsy_lbqy_qydj-2',
								'Host':'guba.eastmoney.com',
								'Referer':'http://guba.eastmoney.com/default,0_1.html'}
		self.page=input('please enter the page number:')
		self.info=[]
	def spider(self,url):
		response=requests.get(url,headers=self.headers).text
		return response

	def datacleaning(self,response):
		
		item={}
		res=etree.HTML(response)
		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[1]/cite[1]/text() readtimes
		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[2]/cite[1]/text()
		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[3]/cite[1]/text()

		read=res.xpath(r'//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul//li/cite[1]/text()')

		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[1]/cite[2]/text()
		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[2]/cite[2]/text()

		comments=res.xpath(r'//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul//li/cite[2]/text()')

		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[1]/span/a[2]
		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[2]/span/a[2]

		title=res.xpath(r'//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul//li/span/a[2]/text()')


		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[1]/cite[3]/a/font
		#//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li[2]/cite[3]/a/font

		author=res.xpath(r'//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul//li/cite[3]/a/font/text()')
		#print(author)
		for i in range(len(read)):
            #for r,c,t,a in zip(read,comments,title,author):#也有个很傻的问题，在这里迭代的时候python很容易认为后面的是一个tuple也就是too many values to unpack
			item['阅读量']=read[i].strip()                      #for r,c,t,a in （read,comments,title,author）如果要让他正确依次迭代需要用zip函数，然后才是按照顺序依次取出来
			item['评论数量']=comments[i].strip()#strip函数去除首尾空格
			item['标题']=title[i].strip()
			item['作者']=author[i].strip()
			self.info.append(item)#加入到一个list中方便保存
		#print(self.info)

			#self.savedata(item)
		return item
		print('执行完成')
	def savedata(self,data):#写入文件的时候不能直接将list或者dict写入文件，dict可以转化成json格式也就是字符串然后写入文件
		try:
			with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\股吧.txt','a',encoding='utf-8')as f:
				f.write(data)
			print('succeed')

		except Exception as e:
			print('saved fail',e)


	def run(self):
		
		for i in range(len(self.page)):
			realurl=self.url%i
			response=self.spider(realurl)
			result=self.datacleaning(response)
			result=json.dumps(self.info)#但是文件转换成json格式的时候会变成unicode
			self.savedata(result.encode('utf-8').decode('unicode_escape'))#输出的是unicode需要解码一下变成中文
if __name__ == '__main__':
	guba=Guba()
	guba.run()


