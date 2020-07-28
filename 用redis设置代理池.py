
#1、存储模块
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'
#设置的思路      
# 分数 100 为可用，检测器会定时循环检测每个代理可用情况，一旦检测到有可用的代理就立即置为 100，检测到不可用就将分数减 1，减至 0 后移除。
# 新获取的代理添加时将分数置为 10，当测试可行立即置 100，不可行分数减 1，减至 0 后移除。
# 这是一种解决方案，当然可能还有更合理的方案。此方案的设置有一定的原因，在此总结如下：
# 当检测到代理可用时立即置为 100，这样可以保证所有可用代理有更大的机会被获取到。你可能会说为什么不直接将分数加 1 而是直接设为最高 100 呢？设想一下，我们有的代理是从各大免费公开代理网站获取的，如果一个代理并没有那么稳定，平均五次请求有两次成功，三次失败，如果按照这种方式来设置分数，那么这个代理几乎不可能达到一个高的分数，也就是说它有时是可用的，但是我们筛选是筛选的分数最高的，所以这样的代理就几乎不可能被取到，当然如果想追求代理稳定性的化可以用这种方法，这样可确保分数最高的一定是最稳定可用的。但是在这里我们采取可用即设置 100 的方法，确保只要可用的代理都可以被使用到。
# 当检测到代理不可用时，将分数减 1，减至 0 后移除，一共 100 次机会，也就是说当一个可用代理接下来如果尝试了 100 次都失败了，就一直减分直到移除，一旦成功就重新置回 100，尝试机会越多代表将这个代理拯救回来的机会越多，这样不容易将曾经的一个可用代理丢弃，因为代理不可用的原因可能是网络繁忙或者其他人用此代理请求太过频繁，所以在这里设置为 100 级。
# 新获取的代理分数设置为 10，检测如果不可用就减 1，减到 0 就移除，如果可用就置 100。由于我们很多代理是从免费网站获取的，所以新获取的代理无效的可能性是非常高的，可能不足 10%，所以在这里我们将其设置为 10，检测的机会没有可用代理 100 次那么多，这也可以适当减少开销。 
import redis
from random import choice
 
class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)#这是redis-py用于实现redis的命令--StrictRedis
 
    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):#返回在这个有序的集中，这个proxy的分数，如果不存在那么用zadd添加
            return self.db.zadd(REDIS_KEY, score, proxy)
 
    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)#zrangebyscore，通过分数返回有序集合指定区间内的成员
        if len(result):#如果有最高分数的存在，则随机选择一个
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)#zrevrange方法，返回有序集中指定区间内的成员，通过索引，分数从高到低
            if len(result):#如果存在的话，随机选择一个
                return choice(result)
            else:
                raise PoolEmptyError
 
    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)#zscore用于返回有续集中成员的分数值
        if score and score > MIN_SCORE:#判断分数值是否大于最小设置的
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)#zincrby(increment增量)，用于对象增加数据，即后面的增加-1
        else:#如果没有的话就设置成0
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)
 
    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None#zscore返回成员的分数值。如果分数值不存在就返回none
 
    def max(self, proxy):#这个方法设置最大
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
 
    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)#zcard获取里面的代理数量
 
    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)#获取从大到最小的代理
 

 
#2获取模块，通过各大代理网站，进项爬取
import json
from .utils import get_page
from pyquery import PyQuery as pq        
#需要定义一个元类
class ProxyMetaclass(type):
        def __new__(cls,name,bases,attrs):#固定的参数其中attrs代表的是是各个类的各种属性方法，可以用for循环出这个父类下面的所有类的各种属性，初次之外还可以额外加入属性即下面的这两个
            count=0
            attrs['__CrawlFunc__']=[]
            attrs['__CrawlFuncCount']=[]
            for k,v in attrs.items():#遍历字典的时候v就等于value
                if 'crawl_' in k:
                    attrs['__CrawlFunc'].append(k)
                    count+=1#每加入一次就计数加一
            attrs['__CrawlFuncCount']=count
            return type.__new__(cls,name,bases,attrs)
            
            
# 再定义一个爬虫类专门封装爬虫函数
class Crawler(object,metaclass=ProxyMetaclass):
        def get_proxies(self,callback):#通过回调函数名执行对应的方法，返回获取到的所有代理
            proxies=[]
            for func in eval('self.{}()'.formata(callback))#eval函数是动态调用函数的方法，且也能把字符转直接转换成计算单位
                print('获取到代理'，proxy)
                proxies.append(proxy)
            return proxies
            
        def crawl_daili66(self, 4):#开始写爬虫爬取代理页面了
            starturl='http://www.66ip.cn/{}.html'
            for page in range(1,5):
                urls=starturl{}.formate(page)
                #清洗数据这里用的 是pyquery方法，先用.utils import get_page，提取html之后用pyquery也可以试试其他方法#pyquery可以在熟悉一下
                html = get_page(url)
                #get_page需要判断是否为html
                if html:
                    doc=pq(html)
                    trs = doc('.containerbox table tr:gt(0)').items()
                    for tr in trs:
                        ip = tr.find('td:nth-child(1)').text()
                        port = tr.find('td:nth-child(2)').text()
                        yield ':'.join([ip,port])#这一步的join方法，表示在清洗出的ip以及 port之间加入：冒号
        def crawl_proxy360(self):
            starturl='http://www.proxy360.cn/Region/China'
            print('正在爬取：',starturl)
            html=get_page(starturl)
            if html:
                doc = pq(html)
                lines = doc('div[name="list_proxy_ip"]').items()
                for line in lines:
                    ip = line.find('.tbBottomLine:nth-child(1)').text()
                    port = line.find('.tbBottomLine:nth-child(2)').text()
                    yield ':'.join([ip, port])
        def crawl_goubanjia(self):
      
            starturl = 'http://www.goubanjia.com/free/gngn/index.shtml'
            html = get_page(start_url)
            if html:
                doc = pq(html)
                tds = doc('td.ip').items()
                for td in tds:
                    td.find('p').remove()
                    yield td.text().replace(' ', '')
        
#上面已经定义了crawer类，就需要调用抛弃啊        
from db import redis
from crawler import Crawler
POOL_UPPER_THRESHOLD = 10000#这里定义了一个池的容量上限
        
class Getter():
    def __init__(self):
        self.redis=RedisClient()
        self.crawler=Crawler()
        #x判断是否达到了容量吃
    def is_over_threshold():
        if self.redis.count()>=POOL_UPPER_THRESHOLD:
            return Ture
        else:
            return False
    def run(self):#获取装置开始执行
        print('huoquqi开始执行')
        if not is_over_threshold():
            for callbacklabel in range(self.crawler.__CrawlFuncCount):
                callback=self.crawler.__CrawlFunc[callbacklabel]
                proxies=self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
        
#3、设置一个检测模块一般来说可以用requests来进行，但是由于代理的数量非常多，为了提高代理的检测效率，我们在这里使用异步请求库 Aiohttp 来进行检测。        
 VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100
class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
    async def test_single_proxy(self, proxy):
        conn=aiohttp.TCPConnector(verify_ssl=False)#TCPConnector,用于TCPConnector维持链接池，限制并行连接的总量，当池满了，有请求退出再加入新请求。默认是100，limit=0的时候是无限制verify_ssl (布尔类型) –
#对HTTPS请求验证SSL证书(默认是验证的)。如果某些网站证书无效的话也可禁用。(该参数可选)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy=proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法', proxy)
            except (ClientError, ClientConnectorError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)
    def run(self):
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)

















