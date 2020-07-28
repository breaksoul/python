#点触认证例如12306，机器识别难度很大，通过第三方人工识别机构实现，需要费用例如：超级鹰：https://www.chaojiying.com/api-14.html
#先要在官网下载啊apihttps://www.chaojiying.com/api-14.html，
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
 
EMAIL = 'cqc@cuiqingcai.com'#网站的登录
PASSWORD = ''

CHAOJIYING_USERNAME = 'Germey'#超级鹰的登录
CHAOJIYING_PASSWORD = ''
CHAOJIYING_SOFT_ID = 893590
CHAOJIYING_KIND = 9102

class CrackTouClick():
    def __init__(self):
        self.url = 'http://admin.touclick.com/login.html'
        self.webdriver=webdriver.Chrome()
        self.wait=WebdriverWait(self.browser, 20)
        self.email=EMAIL
        self.password=PASSWORD
        self.chaojiying=CAHOJIYING(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)#超级鹰中需要传入的三个参数
        
    #开始获取验证码，先填入表单之后模拟点击呼出验证
    def open(self):
        self.browser.get(self.url)
        email=self.until.wait(EC.presence_of_element_located(By.ID,'email'))
        email.send_keys(self.email)
        password=self.until.wait(EC.presence_of_element_located(By.ID,'password'))
        password.send_keys(self.password)
    
    #获取初始验证码，即点验证按钮出来验证码
    def get_touclick_button(self):
        button=self.wait.until(EC.element_to_be_clickable(By,CLASS_NAME,'touclick-hod-wrap'))
        return button
        d
    #开始截取图片，先获取图片的位置，之后调用get_screenshot,最后在用crop方法
    def get_touclick_element(self):
        element=self.until.wait(EC.prensence_of_element_located(By.CLASS_NAME, 'touclick-pub-content' ))
        return element
    def get_position(self):
        element=self.get_touclick_element()
        lacation=element.location
        size=element.size
        top, bottom, left, right=location(y),location(y)+size('height'),location(x),location(x)+size('weight')
        return (top, bottom, left, right)
    def get_screenshot(self):
        screenshot=self.browser.get_screenshot_as_png()
        screenshot=Image.open(BytesIO(screenshot))#把文件转化成utf08bianma的字节，然后打开
        return screenshot
    def get_touclick_image(self, name='captcha.png'):#先给图片名字赋予一个名字captcha.png'):#
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot=self.get_screenshot()
        captcha==screenshot.crop((left, top, right, bottom))
        return captcha
        
        
    #开始识别验证码，然后调用Chaojiying 对象的 post_pic() 方法即可把图片发送给超级鹰后台
    def 
        
        
    #识别成功后会返回一个json数据，{'err_no': 0, 'err_str': 'OK', 'pic_id': '6002001380949200001', 'pic_str': '132,127|56,77', 'md5': '1f8e1d4bef8b11484cb1f1f34299865b'} 
    #其中 pic_str 就是识别的文字的坐标，是以字符串形式返回的，每个坐标都以 | 分隔
    def get_points(self,captcha_result):
        groups = captcha_result.get('pic_str').split('|')#得到的pic_str之后以再‘|’切割出来即可得到每个验证汉字的坐标（）案例是两个所以得到两个坐标
        locations = [[int(number) for number in group.split(',')] for group in groups]#先计算后面的，group，之后吧后面的坐标按照，分开切出来的两个坐标，在按照‘，’分割就相当于（x,y）分成了x，yield
        return locations
    def touch_click_words(self, locations):
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(),location[0], location[1]).click().perform()
            time.sleep(1)
    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, '_submit')))
        submit.click()
        time.sleep(10)
        print('登录成功')
    
    def crack(self):
        """
        破解入口
        :return: None
        """
        self.open()
        # 点击验证按钮
        button = self.get_touclick_button()
        button.click()
        # 获取验证码图片
        image = self.get_touclick_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 识别验证码
        result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        # 判定是否成功
        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'touclick-hod-note'), '验证成功'))
        print(success)
        
        # 失败后重试
        if not success:
            self.crack()
        else:
            self.login()


if __name__ == '__main__':
    crack = CrackTouClick()
    crack.crack()
#这部分是超级鹰的代码，是官方给的，需要放在另外一个文件中调用    
# import requests
# from hashlib import md5


# class Chaojiying(object):

    # def __init__(self, username, password, soft_id):
        # self.username = username
        # self.password = md5(password.encode('utf-8')).hexdigest()
        # self.soft_id = soft_id
        # self.base_params = {
            # 'user': self.username,
            # 'pass2': self.password,
            # 'softid': self.soft_id,
        # }
        # self.headers = {
            # 'Connection': 'Keep-Alive',
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        # }
        

    # def post_pic(self, im, codetype):
        # """
        # im: 图片字节
        # codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        # """
        # params = {
            # 'codetype': codetype,
        # }
        # params.update(self.base_params)
        # files = {'userfile': ('ccc.jpg', im)}
        # r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        # return r.json()

    # def report_error(self, im_id):
        # """
        # im_id:报错题目的图片ID
        # """
        # params = {
            # 'id': im_id,
        # }
        # params.update(self.base_params)
        # r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        # return r.json()

# z    
    
    

#上面是写的，下面的是原始代码
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying

EMAIL = 'cqc@cuiqingcai.com'
PASSWORD = ''

CHAOJIYING_USERNAME = 'Germey'
CHAOJIYING_PASSWORD = ''
CHAOJIYING_SOFT_ID = 893590
CHAOJIYING_KIND = 9102


class CrackTouClick():
    def __init__(self):
        self.url = 'http://admin.touclick.com/login.html'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
    
    def __del__(self):
        self.browser.close()
    
    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)
    
    def get_touclick_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'touclick-hod-wrap')))
        return button
    
    def get_touclick_element(self):
        """
        获取验证图片对象
        :return: 图片对象
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'touclick-pub-content')))
        return element
    
    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        element = self.get_touclick_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)
    
    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot
    
    def get_touclick_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha
    
    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations
    
    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0],
                                                                   location[1]).click().perform()
            time.sleep(1)
    
    def touch_click_verify(self):
        """
        点击验证按钮
        :return: None
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'touclick-pub-submit')))
        button.click()
    
    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, '_submit')))
        submit.click()
        time.sleep(10)
        print('登录成功')
    
    def crack(self):
        """
        破解入口
        :return: None
        """
        self.open()
        # 点击验证按钮
        button = self.get_touclick_button()
        button.click()
        # 获取验证码图片
        image = self.get_touclick_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 识别验证码
        result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        # 判定是否成功
        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'touclick-hod-note'), '验证成功'))
        print(success)
        
        # 失败后重试
        if not success:
            self.crack()
        else:
            self.login()


if __name__ == '__main__':
    crack = CrackTouClick()
    crack.crack()
