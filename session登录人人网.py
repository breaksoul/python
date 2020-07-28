import requests

base_url = 'http://www.renren.com/PLogin.do'
headers= {
    'Host': 'www.renren.com',
    'Referer': 'http://safe.renren.com/security/account',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}
data = {
    'email':邮箱,
    'password':密码,
}
#创建一个session对象
se = requests.session()
#用session对象来发送post请求进行登录。
se.post(base_url,headers=headers,data=data)
response = se.get('http://www.renren.com/971682585')

if '鸣人' in response.text:
    print('登录成功！')
else:
    print(response.text)
    print('登录失败！')
