#案例一，模拟淘宝并等待2秒随后返回源代码

3
4
5
function main(splash)
    splash:go("https://www.taobao.com")
    splash:wait(2)
    return {html=splash:html()}
end