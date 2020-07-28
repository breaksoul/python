import requests
from lxml import etree
import threading
from queue import Queue
import time
#多线程需要重构run函数，需要写
class Maoyan(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)#线程初始化，领娃还有个super的初始化
        self.url='http://maoyan.com/board/4?offset='
        self.name=name
        self.page=page
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
         'Host': 'maoyan.com',
         'Cookies':'__mta=44372763.1588144593946.1588236323384.1588237149852.13; uuid_n_v=v1; uuid=4FE2082089E911EAA2F9D99FA42ECE4AF9128CD739BF4F1B9BBF99D60ADF0AC9; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; _lxsdk_cuid=171c4cb5b8cc8-068f6a4009a924-3c375c0f-100200-171c4cb5b8dc8; _lxsdk=4FE2082089E911EAA2F9D99FA42ECE4AF9128CD739BF4F1B9BBF99D60ADF0AC9; t_lxid=171c4cb5c0dc8-03b48fbdcf5b63-3c375c0f-100200-171c4cb5c0dc8-tid; mojo-uuid=36ccb7d82f878fb133911bace2232100; __mta=44372763.1588144593946.1588144657604.1588144768667.5; _csrf=a548620cf980995ddcfab224224bc0018af6747a808af5474eb5086b0ccbb96e; mojo-session-id={"id":"dea887e69fa39008008e5546ea8c0979","time":1588236299991}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1588144594,1588236300; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1588237150; _lxsdk_s=171ca42afdb-4ad-16d-487%7C%7C6'}
        self.items=[]
        #print('初始化变量完成')
    def spider(self,realurl,headers):
        response=requests.get(realurl,headers=self.headers).text
        #print('spider完成')
        return response
    def qingxi(self,response):
        html=etree.HTML(response)
        nameresult=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/div/div//div//p/a/text()')
        starresult=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/div/div//div//p[2]/text()')
        result=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/i/text()')
        releasetime=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/div/div//div//p[3]/text()')
        for i in range(len(nameresult)):
            self.items.append(nameresult[i]+starresult[i]+result[i]+releasetime[i])#多个列表一一对应拼接放到一个list中
        #print('清洗完成',nameresult,starresult)
        return self.items
    def saved(self,items):
        for n in items:
            with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\猫眼top100.txt','a',encoding='utf-8') as f:
                f.write(n)
# a 追加模式  不会清空原来的内容 追加写，但是不能读

# r+ 读写模式  文件不存在的时候会报错   可读可写，但是写的有问题（在最前方写，因为指针在0处）

# w+ 写读模式   文件不存在的时候给创建  清空文件内容，然后在写

# a+ 追加模式   文件不存在的时候给创建  可读可写  ，追加写，但是读不到内容（因为指针在末尾，所以读不到）
        #print('文件保存完成')
#调用内部函数需要加上self否则会被当成外部函数
    def run(self):
        #print('开始执行')
        for i in range(int(page)):
            realurl=self.url+str((i*10))
            #print(realurl)
            response=self.spider(realurl,self.headers)
            items=self.qingxi(response)
            saved=self.saved(items)
        
if __name__ == '__main__':
    
    page=input('请输入需要的页码：')
    start = time.time()
#创建任务队列
    q=Queue()
    #添加任务，任务为需要爬取的页码，也就是说每页一个线程
    for i in range(int(page)):
        q.put(i)
    crawl_list = ['aa','bb','cc','dd','ee']
    list_ = []
    for name in crawl_list:
        maoyan=Maoyan(name)
        maoyan.start()
        list_.append(maoyan)
        print('%s 正在运行' % threading.current_thread().name)#返回当前线程
        
    print('%s 运行的线程数目' % threading.activeCount())#返回正在运行的线程数量，与len(threading.enumerate())有相同的结果    
    for l in list_:
        l.join()
    print(print(time.time()-start))

    
    
