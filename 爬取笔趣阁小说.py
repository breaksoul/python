#保存有错误，每个文件都全部保存了所有文件 for循环问题
import requests
from lxml import etree
#爬取循环小说排行榜

url='http://www.xbiquge.la/paihangbang'
base_url='http://www.xbiquge.la'

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
#'Cookies': ' _abcde_qweasd=0; _abcde_qweasd=0; bdshare_firstime=1592016287393; Hm_lvt_169609146ffe5972484b0957bd1b46d6=1592016287,1592104155,1592111209,1592711534; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1592711552',
#'Host': 'www.xbiquge.la',
#'Referer': 'http://www.xbiquge.la/xiaoshuodaquan/'
response=requests.get(url,headers=headers).text

#print(response)#测试返回正确数据
#清洗数据
html=etree.HTML(response)
#novelname=html.xpath(r'//*[@id="main"]/div[2]/ul[1]/li[position()>=2 and position()<=20]/a/text()')
novellinks=html.xpath(r'//*[@id="main"]/div[2]/ul[1]/li[position()>=2 and position()<=20]/a/@href')

#print(novelname,novellinks)#可以获取
#//*[@id="main"]/div[2]/ul[1]/li[position()>=2]/a/@href#小说链接
#//*[@id="main"]/div[2]/ul[1]/li[position()>=2]/a/text()
count=0
for link in novellinks:#获取到了小说链接
	#一个item就是一本书
	res=requests.get(link).text
	#print(res.encoding)
	res=res.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res)[0])
	result=etree.HTML(res)
	#//*[@id="info"]/h1书名
	novelname=result.xpath(r'//*[@id="info"]/h1/text()')
	contenttitle=result.xpath(r'//*[@id="list"]/dl/dd[1]/a/text()')
	contentlinks=result.xpath(r'//*[@id="list"]/dl/dd[1]/a/@href')#获取第一章的href，换成下面的就是获取所有

	#//*[@id="list"]/dl/dd[2]/获取所有章节名称列表
	count+=1
	print('开始获取小说链接',count)
	#/15/15409/8163818.html
	for n in range(len(contentlinks)):#获取到小说章节链接
		item={}
		contentlink=base_url+contentlinks[n]
		
		conres=requests.get(contentlink).text
		#print(conres.encoding)
		conres=conres.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(conres)[0])
		#print(conres.status_code)
		# 内容的xpath//*[@id="content"]/text()[1]
		conres=etree.HTML(conres)
		conresult=''.join(conres.xpath(r'//*[@id="content"]//text()'))#用空格链接各个文字,就能去掉list变成字符
		
		#//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()
		#//*[@id="list"]/dl/dd[1]/a
		#//*[@id="wrapper"]/div[4]/div/div[2]/h1
		#contenttitle=conres.xpath(r'//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()')获取第一行错误，空白
		#print(len(conresult))
		#print(contenttitle)
		item['content']=conresult
		item['title']=contenttitle[n]
		#for n in range(len(contenttitle)):
			
			
		#print(len(item))
		print('开始保存',count)

		with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\new pen fun\{}.txt'.format(novelname),'a+',encoding='utf-8')as f:
			f.write(item['title'].replace('','\n'))
			#可以尝试用strip函数清楚前后的空格
			f.write(item['content'].strip())#内容中的空格替换成换行，注意上面的join函数将每个字之间也变成了空格字符

	


	#//*[@id="list"]/dl/dd[1]/a 章节链接和章节名称
