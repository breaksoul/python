#百度翻译，有个sign，这个就导致不能外部随便更改翻译内容，经过测试，请求头中必须要cookie，不然没法成功获取网页信息
import requests
import json
import re
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
         'cookie':'BAIDUID=4DE204336476C9DED0A82BF975777C70:FG=1; BIDUPSID=4DE204336476C9DED0A82BF975777C70; PSTM=1563365731; BDUSS=3g0eDZrZWY1elpaSk1IaWUzWUZWQ0JVTTdzNDhOaU9WeUF4ZFVLMUI1NWFTWkZkRVFBQUFBJCQAAAAAAAAAAAEAAABvJU07bG92ZXN5MTk5NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFq8aV1avGldV; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1587215137,1587713932; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1587714111; yjs_js_security_passport=37b956ff81c5fca7430415033fe084975ad6ba87_1587714096_js; delPer=0; PSINO=1; H_PS_PSSID=1444_31169_21083_31427_31341_30904_31228_30823_31085_26350_31164_31195; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598'}
url='https://fanyi.baidu.com/v2transapi?from=zh&to=en'
#https://fanyi.baidu.com/?#zh/en/%E4%BD%A0%E5%A5%BD'
#https://fanyi.baidu.com/v2transapi?from=zh&to=en  

key="你好"
#formdata={
#'kw'='你好'
#}

formdata={
'from':'zh',
'to':'en',
'query':'你好',
'transtype':'enter',
'simple_means_flag':'3',
'sign':'232427.485594',#不同的翻译类容会变化，所以只能用一个翻译，不能更改翻译类容，解决方法还不知道
'token':'b51588f264b5f3a8e8354a8c6b54ea63',
'domain':'common',
}
response=requests.post(url,data=formdata,headers=headers)
if response.status_code==200:#查看网页返回状态吗，是不是200，不是200代表有错误
    print('返回正确')
else:
    print(response.status_code)#这个代码有点问题，网页返回码是401#解决：因为没有cookie，加上之后就ok了
#print(response.content.decode('unicode_escape'))
#正则表达式清洗数据
pat=r'{"dst":"(.*?)","'
pattern=re.compile(pat)
result=pattern.findall(response.text)#解析的时候需要将它转化为字符串否则有报错
print(result)

#网页有个sign只能通过反向so解密实现，可以在页面用ctri用f搜索


#response.content.decode(‘unicode_escape’)：当相应结果中存在中文的时候，利用这种编码格式进行转码
#因为最后的数据是json格式，必须要用json解码一次，如果忘了加括号就会<bound method Response.json of <Response [410]>>
#百度翻译是，post方法，上传的data表也没问题，但是为什么拿不到信息
#获取response的数据有2种方式 一种是text获取的直接是文本格式 但是可能有乱码 需要手动设置response.encoding("编码") 解决乱码 
#还有一种就是response.content 里面存的是网站直接返回的数据 二进制格式 然后通过decode解码即可
#因为返回的是json对象，所以我们将最后解码后的字符串进行json格式转换 使用json.loads()进行转换
#1 import json
#2 json.load() # 将一个存储在文件中的json对象（str）转化为相对应的python对象
#3 json.loads() # 将一个json对象（str）转化为相对应的python对象
#4 json.dump() # 将python的对象转化为对应的json对象（str),并存放在文件中
#5 json.dumps() # 将python的对象转化为对应的json对象（str)
#response.content.decode(‘unicode_escape’)：当相应结果中存在中文的时候，利用这种编码格式进行转码
