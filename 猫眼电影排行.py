import requests
from lxml import etree


#爬取top100榜单，offset=i*10


headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
         'Host': 'maoyan.com',
         'Cookies':'__mta=44372763.1588144593946.1588236323384.1588237149852.13; uuid_n_v=v1; uuid=4FE2082089E911EAA2F9D99FA42ECE4AF9128CD739BF4F1B9BBF99D60ADF0AC9; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; _lxsdk_cuid=171c4cb5b8cc8-068f6a4009a924-3c375c0f-100200-171c4cb5b8dc8; _lxsdk=4FE2082089E911EAA2F9D99FA42ECE4AF9128CD739BF4F1B9BBF99D60ADF0AC9; t_lxid=171c4cb5c0dc8-03b48fbdcf5b63-3c375c0f-100200-171c4cb5c0dc8-tid; mojo-uuid=36ccb7d82f878fb133911bace2232100; __mta=44372763.1588144593946.1588144657604.1588144768667.5; _csrf=a548620cf980995ddcfab224224bc0018af6747a808af5474eb5086b0ccbb96e; mojo-session-id={"id":"dea887e69fa39008008e5546ea8c0979","time":1588236299991}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1588144594,1588236300; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1588237150; _lxsdk_s=171ca42afdb-4ad-16d-487%7C%7C6'}

url='http://maoyan.com/board/4?offset='


page=input('请输入爬取的页码数量')


for i in range(int(page)):
    realurl=url+str((i*10))
    
    response1=requests.get(realurl,headers=headers).text
    #print(response1.encoding)#这个检测代码编码方式的时候，需要是源代码，text文本不行
    
    response=response1.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(response1)[0])
    print(response)
    
    html=etree.HTML(response)
    nameresult=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/div/div//div//p/a/text()')
    
    
    starresult=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/div/div//div//p[2]/text()')
    result=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/i/text()')
    releasetime=html.xpath(r'//*[@id="app"]/div/div//div/dl//dd/div/div//div//p[3]/text()')
    print(nameresult,starresult,result,releasetime)
    for a in range(len(nameresult)):
        name=nameresult[a].replace(' ','')
        star=starresult[a].replace(' ','')
        paiming=result[a].replace(' ','')
        time=releasetime[a].replace(' ','')     
        print ('排名：%s  电影名称：%s  主演：%s  上映时间：%s  '%(paiming,name,star,time),sep='&',end='---\n\n')
#通过格式化输出的方式让输出的东西更加美观，上面的replace函数，代替了多余的空格
    #print(nameresult,starresult,result,releasetime)

        #try:
            #with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\猫眼top100.txt',wb,encoding='utf-8') as f:#细节很重要转义
                #f.write(name,star,paiming,time)
            #print('写入成功')
        #except Exception as e:
            #print(e,'写入错误')



  
    
    
    #电影名称//*[@id="app"]/div/div/div[1]/dl/dd[1]/div/div/div[1]/p[1]/a/text()  总结
    #//*[@id="app"]/div/div/div[1]/dl/dd[2]/div/div/div[1]/p[1]/a
    #//*[@id="app"]/div/div//div/dl//dd/div/div//div//p/a
    
    #主演//*[@id="app"]/div/div//div/dl//dd/div/div//div/p[class="star"]/text()
    #//*[@id="app"]/div/div/div[1]/dl/dd[2]/div/div/div[1]/p[2]
   
    #电影排名//*[@id="app"]/div/div/div[1]/dl/dd[1]/i
    #//*[@id="app"]/div/div/div[1]/dl/dd[2]/i
    
    #上映时间//*[@id="app"]/div/div//div/dl//dd/div/div//div/p[class="releasetime"]/text()
    
    
    
    
    
