import requests
from lxml import etree
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
content=input('请输入搜索内容:')
pages=int(input('请输入页码：'))
for page in range(pages):
        url='https://search.sina.com.cn/?q=%s&c=news&from=channel&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=%s'%(str(content),str(page))
        response1=requests.get(url,headers=headers)
        #print(response1.text)
        
        html=etree.HTML(response1.text)
        results=html.xpath('//*[@id="result"]//div/h2/a/@href')#//*[@id="result"]/div[4]/h2/a,直接copy下来的但是有点不对//*[@id="result"]/*[class="box-result clearfix"]/h2/a@href
#直接复制更改的//*[@id="result"]/div[4]/h2/a
        #print(results)
#自己写的//div[class="wrap"]/div[class="main clearfix"]/div[class="result"]//div[class="box-result clearfix"]/h2/a@href'

        for result in results:
                response2=requests.get(result,headers=headers).text
                #print(response2.encoding)#返回的内容中的编码格式，很明显最后打印的内容中出现乱码就是这个编码的锅
                #print(response2.headers['content-type'])#文件的类型
                #print(response2.apparent_encoding)#responseheader中设置的编码类型
                #print(requests.utils.get_encodings_from_content(response2.text))#返回的header标签中设置的编码
                #输出的结果分别是，
                #ISO-8859-1
                #text/html
                #utf-8
                #['utf-8']
                response2 = response2.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(response2)[0])#这一步成功的解决了后续的问题
                html=etree.HTML(response2)
                results2=html.xpath('//*[@id="artibody"]//p/font/text()')#//*[@id="artibody"]/p[1]/font/text()
                print(results2)
                
                for r in results2:
                        
                        try:
                                with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\新浪消息.txt','a',encoding='utf-8') as f:#用withopen会自动关闭文件，不需要在写f.close
                                        f.write(r)
                        except Exception as e:#f.write必须要是一个字符串，不能直接写入list，xpath直接清洗出来的是一个list
                                print('出错',e)
print("写入完成")
#抓到的内容打印出来有些不对例如x8cçº§å\x88«è½¦ä¸\xadæ\x9c\x89ä¸\x8dé\x94\x99ç\x9a\x84æ\x80§ä»·æ¯\x94ã\x80\x82å¯¹äº\x8eè¿\x99æ¬¾å¤§å\x8e\x82ç\x9a\x84å®\                   
#原因是requests会简单的从服务器返回的响应头中content-type中获取编码，其中必须要包括charset才能正常识别，否则就使用默认编码iso-8859-1.
#解决方法，request内部提供了一个utils从返回的body中获取页面编码的函数，即get_encodings_from_content,这样即使返回的不包含charset也能识别出正确编码
#即，可以用print(r.encoding)先查看编码，然后在通过r = r.text.encode('查出来的返回的内容编码格式写在这').decode(requests.utils.get_encodings_from_content(r.text)[0])设置编码
#response2=requests.get(result,headers=headers).text
#print(response2.encoding)#返回的内容中的编码格式，很明显最后打印的内容中出现乱码就是这个编码的锅
#print(response2.headers['content-type'])#文件的类型
#print(response2.apparent_encoding)#responseheader中设置的编码类型
#print(requests.utils.get_encodings_from_content(response2.text))#返回的header标签中设置的编码
                #输出的结果分别是，
                #ISO-8859-1
                #text/html
                #utf-8
                #['utf-8']
