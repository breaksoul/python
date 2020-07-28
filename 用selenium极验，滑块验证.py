from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from PIL import Image
from selenium.webdriver.common.by import By

EMAIL = 'test@test.com'
PASSWORD = '123456'
url='https://account.geetest.com/login'
header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}
BORDER = 6
INIT_LEFT = 60

class CrakGeetest():
    def __init__(self):
        self.browser=webdriver.Chrome()
        self.url=url
        self.wait=WebdriverWait(self.browser,10)
    
    # def tiqucookies(self):
        # session= requests.Session()#session 可以自动处理cookies不用再自己提交
        # response=session.get(url,headers=header)
        # response1 = requests.get(url, headers=headers)
        # if response1.status_code == 200:
        #   cookies = response1.cookies
        #   print(cookies)
        #表单提交上去response2 = requests.post(url, data=data, headers=headers, cookies=cookies)
        
    def getgeetestbutton():
        button=self.wait.until(EC.element_to_be_clickable(By.CLASS_NAME,'geetest_radar_tip'))
        return button
    
    def get_position(self):
        img=self.wait.until(EC.presence_of_element_located(By.CLASS_NAME,'geetest_canvas_slice geetest_absolute'))#找到原图片的位置
        location=img.location#定位图片在浏览器中的位置（以左上角作为原点，y向下递增，x右递增，最后是个字典的形式{x:33,y:66}）
        size=img.size#图片的大小anzhao 长宽分布size[0]取第一个
        top,bottom,left,right=location(y),location(y)+size('height'),location(x),location(x)+size('width')
        return (top,bottom,left,right)
    #完整的图片，网站有改版
    
    def get_geetest_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()
        print('验证码位置',top, bottom, left, right)
        screenshot = self.get_screenshot()#截图方法
        captcha = screenshot.crop((left, top, right, bottom))#剪裁方法crop，返回一个矩形区域的拷贝
        captcha.save(name)
        return captcha
    
    def get_slider():
        slider=self.until.wait(EC.element_to_be_clickable(By.CLASS_NAME,'geetest_slider_button'))
        return slider
        #之后再调用getgeetestimagefangfa 再次截图可以得到缺口图片
        
    def is_pixel_equal(self,image1, image2, x, y):
    #遍历2张图片的每个像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]#load（）方法主要返回一个用于读取和修改像素的像素访问对象。这个访问对象像一个二维队列
        #例如：>>>from PIL import Image

                ##>>>im01 = Image.open("D:\\Code\\Python\\test\\img\\test01.jpg")

                #>>> pix= im01.load()

                #>>>pix[0,0]

                #(11, 113, 198)
        threshold = 60
        #获取到了两张图片对应像素点的 RGB 数据，然后判断二者的 RGB 数据差异，如果差距超过在一定范围内，那就代表两个像素相同，继续比对下一个像素点，如果差距超过一定范围，则判断像素点不同，当前位置即为缺口位置
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:#经过上面的image.load（）[x.y]之后会将每个点的坐标转化为rgb的格式[R,G,B]三个参数，需要对比每个颜色是否一致即可确认是否为一样的点
            
            return True
        else:
            return False
    
    
    def get_gap(self,image1,image2):
        left = 60#设置这个值是为了从滑块的右侧开始遍历图片的坐标点，缺口只会出现在滑块的右侧
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left=i#拿到不对等的坐标就是缺口位置，之后打印出位置
                    return left
    
    
    
    #模拟拖动 滑块 做匀加速之后到匀减速运动
    def get_track(self,distance)
        #移动轨迹
        track=[]#记录了每个时间间隔移动了多少位移，这样滑块的运动轨迹就得到了。
        #当前的位移
        current=0
        #减速阈值
        mid=distance*4/5
        #计算间隔
        t=0.2
        #初速度
        v=0
        while current<distant:
            if current<mid:
                a=2
            else:
                a=-3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move    
        
    #按照该运动轨迹拖动滑块
    def move_to_gap(self,slider,track):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
        
    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        time.sleep(10)
        print('登录成功')
        
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

        
    def crack(self):
        # 输入用户名密码
        self.open()
        # 点击验证按钮
        button = self.getgeetestbutton()
        button.click()
        # 获取验证码图片
        image1 = self.get_geetest_image('captcha1.png')
        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()
        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)#k可以在理解理解
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)
        
        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        print(success)
        
        # 失败后重试
        if not success:
            self.crack()
        else:
            self.login()    
        
    
if __name__ == '__main__':
crack = CrackGeetest()
crack.crack()    
        
    
    
    
# 点按呼出缺口,网站需要点击滑块才出现缺口图片不过好像不用了现在
# slider = self.get_slider()
# slider.click()
#


# button = self.get_geetest_button()
# button.click()
  
    
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from lxml import etree
# import time