#问题在于微博现在改版，page页现在变成了since——id搞不定
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq

baseurl="http://m.weibo.cn/api/container/getIndex?"
#主要有三个传入的type=uid
#&value=2830678474
#&containerid=1076032830678474"
#type=uid
#since_id,这个还没找到解决办法
header={
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',}

# containerid: "1076032830678474"
# show_style: 1
# since_id: 4452242016819175 微博当时第一条的sinceid，sinceid代表的是每格微博的改成page也是可以的d,

# v_p: 42

def get_page(page):
    parms={'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page':page}
    url=baseurl+urlencode(parms)
    try:
        res=requests.get(url,headers=header)
        if res.status_code==200:#判断响应的状态码
            return res.json()
            
    except  exception as e:
        print (e)
        
#需要获取微博的点赞数，事实上这些信息是藏在mblog里面        

def parse_page(json):

    if json:
        items=json.get('data').get('cards')
        
        for item in items:
            item = item.get('mblog')
            weibo={}
            weibo['id']=item.get('id')
            weibo['text']=pq(item.get('text')).text()#可以用pq(item.get('text')).text()清洗里面的html标签
            weibo['comments']=item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo
            
if __name__ == '__main__':
    for page in range(1, 3):#这个还不知道直接放一部分直接遍历能不能拿到
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)            
#存入到 manggodb数据库

#from pymongo import MongoClient
# client = MongoClient()
# db = client['weibo']
# collection = db['weibo']
 
# def save_to_mongo(result):
    # if collection.insert(result):
        # print('Saved to Mongo')
