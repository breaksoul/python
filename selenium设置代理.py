from selenium import webdriver

proxy=' 127.0.0.1:9743'
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--proxy_server=http://'+proxy)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://httpbin.org/get')