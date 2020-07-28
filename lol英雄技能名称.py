import requests
from lxml import etree
from selenium import webdriver
import json
#第一，先爬取各个英雄的href以及英雄名称
print('开始获取英雄id...')
url='http://lol.qq.com/data/info-heros.shtml'
herourl='http://game.gtimg.cn/images/lol/act/img/js/hero/'
driver=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get(url)


#英雄界面拼接
headers={'Accept': 'application/json, text/javascript, */*; q=0.01',
'Origin': 'http://lol.qq.com',
'Referer': 'http://lol.qq.com/data/info-defail.shtml?id='+str(id),
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
html=etree.HTML(driver.page_source)
#数据清洗
#//*[@id="jSearchHeroDiv"]//li/a/@href
#//*[@id="jSearchHeroDiv"]/li[2]/@href
herolinks=html.xpath(r'//*[@id="jSearchHeroDiv"]//li/a/@href')
#//*[@id="jSearchHeroDiv"]//li/a/p/text()
heroname=html.xpath(r'//*[@id="jSearchHeroDiv"]//li/a/p/text()')
#print(herolinks,heroname)
#爬取到的类型'info-defail.shtml?id=1', 'info-defail.shtml?id=2'#可以用split分割出id，事实上这个网好像不用，因为是按照顺序排列
#split('分割的字符'，-1或者1就是全部分割或者分成两份)
#获取英雄技能名称
#运动了动态加载，ajax访问
#http://game.gtimg.cn/images/lol/act/img/js/hero/1.js
hero_list=[]
print('开始获取英雄名称及技能...')
for link in herolinks:
	id=link.split('=',-1)[-1]
	baseurl=herourl+id+'.js'
	skillres=requests.get(baseurl,headers=headers)#返回的是json格式的函数
	#print(skillres)
	#json.loads是把字符数据转化为一个dict，json。dumps是吧dict转化为普通的字符串
	result=json.loads(skillres.text)
	item_name={}
	heroname=[]
	#开始拼接名字，返回的数据中是dict嵌套dict的形式可以采用{"hero":{"heroId":"2","name":"\u72c2\u6218\u58eb","alias":"Olaf","title":"\u5965\u62c9
	item_name['英雄名称']=result['hero']['name']+''+result['hero']['title']
	#最后再存入一个list中
	heroname.append(item_name)
	#技能在返回的数据中最多需要在用一个for循环,数据中关于技能的描述是spells
	for skill in result['spells']:
		item_skills={}
		item_skills['技能名称']=skill['name']+':'+skill['description']
		heroname.append(item_skills)#再把技能推送到hero这个list中，注意这个时候这个list中推送了这个英雄的item_name，以及这个英雄的item_skills，也就是说只是一个英雄的接受
	hero_list.append(heroname)#再把这一个英雄的介绍推送到一个总的list中即可
print('开始保存技能...')	
hero_list=json.dumps(hero_list)

with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\lol英雄技能.txt','w',encoding='utf-8') as f:
	f.write(hero_list.encode('utf-8').decode('unicode_escape'))
print('保存完成')


