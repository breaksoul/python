#腾讯招聘ajax加载，可以构造请求，所谓的ajax就是需要找到请求的东西就可以
#也可以直接用selenium，这里尝试ajax
import requests
import time
from urllib import parse
import json
url='https://careers.tencent.com/tencentcareer/api/post/ByHomeCategories?'
#请求timestamp=1588831107622&num=6&language=zh-cn

params={'timestamp':time,
'num':'6',
'language':'zh-cn'}

#需要构造的就是这个时间戳直接可以用time。time（）生成，一般取13位需要*1000取小数点前面的直接取整数即可int（time。time（））
time=str(int(time.time()*1000))
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
'cookie':'pgv_pvi=2819949568; _ga=GA1.2.1556269406.1567123868; _gcl_au=1.1.1766361660.1587721299',
'referer':'https://careers.tencent.com/home.html'}

real_url=url+parse.urlencode(params)
response=requests.get(real_url,headers).text
#{"Code":200,"Data":[{"CategoryId":"40001","CategoryName":"技术类","PostNumber":2756,"OrderNumber":1},{"CategoryId":"40003","CategoryName":"产品类","PostNumber":1465,"OrderNumber":2},{"CategoryId":"40006","CategoryName":"内容类","PostNumber":73,"OrderNumber":3},{"CategoryId":"40002","CategoryName":"设计类","PostNumber":472,"OrderNumber":4},{"CategoryId":"40005","CategoryName":"销售、服务与支持类","PostNumber":289,"OrderNumber":5},{"CategoryId":"40008","CategoryName":"人力资源类","PostNumber":104,"OrderNumber":6}]}
#这时候的数据还是json状态，不够美观将至美化,通过下面方法，去除‘Data’就成了普通的list嵌套dict
dict=json.loads(response)
print(dict)
infos=[]
for i in dict['Data']:#遍历dict中key为data里面的数值,注意是大写
	CategoryId=i['CategoryId']
	CategoryName=i['CategoryName']
	PostNumber=i['PostNumber']
#print(response)
	item = {}
	item['CategoryId']=CategoryId
	item['CategoryName']=CategoryName
	item['PostNumber']=PostNumber
	infos.append(item)
print(infos)


