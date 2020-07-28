#pyquery 类似于 beautifulsoup 在使用前需要先将html转化为内部文件
#pyquery比起requests更方便的在于可以直接请求url
html = """
<html lang="en">
    <head>
        简单好用的
        <title>PyQuery</title>
    </head>
    <body>
        <ul id="container">
            <li class="object-1">Python</li>
            <li class="object-2">大法</li>
            <li class="object-3">好</li>
        </ul>
    </body>
</html>
"""
from pyquery import PyQuery as pq

doc=pq(html)
#打印id为container的标签id在pq中看成是#
print(doc('#container'))
#打印class为object-1的标签
print(doc('.object-1'))
#打印标签名为body的表亲
print(doc('body'))
#打印第一个li标签，这个标签并不仅仅是标签名，会打印所有的，
print(psedo_doc('li:first-child'))

#打印最后一个li比哦啊齐纳
print(psedo_doc('li:last-child'))
#答应第几个li标签
print(psudo_doc('li:nth-child'))
#打印含有。。。的li标签，比如包含‘好’的li标签
print(pseudo_doc("li:contains('好')"))
#查找标签可以用find方法
print(doc.find('#container'))
#打印id=container的标签的子标签
container = doc.find('#container')
print(container.children())
输出为：
<li class="object-1"/>
<li class="object-2"/>
<li class="object-3"/>


#父辈标签同理用parents（）

#兄弟标签siblings（）

#。attrs传入属性名称，返回属性值，感觉用的不多啊

object_2 = doc.find('.object-2')
print(object_2.attr('class'))
#提起标签的文本，这个用的很多
print(doc.text())
#另外如果想提取某一个，而不像要子标签下的文本可以用remove方法移除子标签例如
container = doc.find('#container')
container.remove('li')
print(container.text())



二、重点二
pyquery中可以直接向url发起请求，得到的直接就是pq转化过的html
from pyquery import PyQuery
PyQuery(url = 'https://www.baidu.com')


2、opener参数作用是告诉pyquery用什么请求库对网址发起请求。常见的请求库如urllib、requests、selenium。这里我们自定义一个selenium的opener。
from pyquery import PyQuery
from selenium.webdriver import PhantomJS
def selenium_opener(url):
    driver=PhantomJS(executable_path = 'phantomjs的路径')
    driver.get(url)
    hrml=driver.page_source
    driver.quit()
    return html
PyQuery(url='https://www.baidu.com/', opener=selenium_opener)#注意函数名是没有扩括号的
    


崔庆才：pyquery


PyQuery的使用
在上一节我们介绍了BeautifulSoup的使用，它是一个非常强大的网页解析库，可有没有觉得它的一些方法使用有点不适应？有没有觉得它的CSS选择器功能没有那么强大？

如果你对WEB有所涉及，如果你比较喜欢用CSS选择器，如果你对jQuery有所了解，那么这里有一个更适合你的解析库——PyQuery。

接下来我们就来感受一下PyQuery的强大之处。

初始化
像BeautifulSoup一样，PyQuery初始化的时候也需要传入HTML数据源来初始化一个操作对象，它的初始化方式有多种，比如直接传入字符串，传入URL，传文件名。下面我们来详细介绍一下。

字符串初始化
html = '''
<div>
<ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
         <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
         <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
print(doc('li'))
运行结果：

<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
在这里我们首先引入了PyQuery这个对象，取别名为pq，然后声明了一个长HTML字符串，当作参数传递给PyQuery，这样就成功完成了初始化，然后接下来将初始化的对象传入CSS选择器，在这个实例中我们传入li节点，这样就可以选择所有的li节点，打印输出可以看到所有的li节点的HTML文本。

URL初始化
初始化的参数不仅可以以字符串的形式传递，还可以传入网页的URL，在这里只需要指定参数为url即可。

from pyquery import PyQuery as pq
doc = pq(url='http://cuiqingcai.com')
print(doc('title'))
运行结果：

<title>静觅丨崔庆才的个人博客</title>
这样的话PyQuery会首先请求这个URL，然后用得到的HTML内容完成初始化，其实就相当于我们用网页的源代码以字符串的形式传递给PyQuery来初始化。

它与下面的功能是相同的：

from pyquery import PyQuery as pq
import requests
doc = pq(requests.get('http://cuiqingcai.com').text)
print(doc('title'))
文件初始化
当然除了传递一个URL，还可以传递本地的文件名，参数指定为filename即可。

from pyquery import PyQuery as pq
doc = pq(filename='demo.html')
print(doc('li'))
当然在这里需要有一个本地HTML文件demo.html，内容是待解析的HTML字符串。这样它会首先读取本地的文件内容，然后用文件内容以字符串的形式传递给PyQuery来初始化。

以上三种初始化方式均可，当然最常用的初始化方式还是以字符串形式传递。

基本CSS选择器
我们首先用一个实例来感受一下PyQuery的CSS选择器的用法。

html = '''
<div id="container">
<ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
         <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
         <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
print(doc('#container .list li'))
print(type(doc('#container .list li')))
运行结果：

<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
<class 'pyquery.pyquery.PyQuery'>
在这里我们初始化PyQuery对象之后，传入了一个CSS选择器，#container .list li，意思是选取id为container的节点内部的class为list的节点内部的所有li节点。然后打印输出，可以看到成功获取到了符合条件的节点。

然后我们将它的类型打印输出，可以看到它的类型依然是PyQuery类型。

查找节点
下面我们介绍一些常用的查询函数，这些函数和jQuery中的函数用法也完全相同。

子节点
查找子节点需要用到find()方法，传入的参数是CSS选择器，我们还是以上面的HTML为例。

from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
print(type(items))
print(items)
lis = items.find('li')
print(type(lis))
print(lis)
运行结果：

<class 'pyquery.pyquery.PyQuery'>
<ul class="list">
    <li class="item-0">first item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
<class 'pyquery.pyquery.PyQuery'>
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
首先我们选取了class为list的节点，然后我们调用了find()方法，传入了CSS选择器，选取其内部的li节点，最后都打印输出即可观察到对应的查询结果，可以发现find()方法会将符合条件的所有节点选择出来，结果的类型是PyQuery类型。

其实find()的查找范围是节点的所有子孙节点，而如果我们只想查找子节点，那可以用children()方法。

lis = items.children()
print(type(lis))
print(lis)
运行结果：

<class 'pyquery.pyquery.PyQuery'>
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
如果要筛选所有子节点中符合条件的节点，比如我们想筛选出子节点中class为active的节点，可以向children()方法传入CSS选择器.active。

lis = items.children('.active')
print(lis)
运行结果：

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
可以看到输出的结果已经做了筛选，留下了class为active的节点。

父节点
我们可以用parent()方法来获取某个节点的父节点，我们用一个实例来感受一下：

html = '''
<div class="wrap">
<div id="container">
<ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
             <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
             <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
container = items.parent()
print(type(container))
print(container)
运行结果：

<class 'pyquery.pyquery.PyQuery'>
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
在这里我们首先用.list选取了class为list的节点，然后调用了parent()方法，得到其父节点，类型依然是PyQuery类型。

这里的父节点是该节点的直接父节点，也就是说，它不会再去查找父节点的父节点，即祖先节点。

但是如果我们想获取某个祖先节点怎么办呢？可以用parents()方法。

from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
parents = items.parents()
print(type(parents))
print(parents)
运行结果：

<class 'pyquery.pyquery.PyQuery'>
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
 <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
在这里我们调用了parents()方法，可以看到输出结果有两个，一个是class为wrap的节点，一个是id为container的节点，也就是说，parents()方法会返回所有的祖先节点。

如果我们想要筛选某个祖先节点的话可以向parents()方法传入CSS选择器，这样就会返回祖先节点中符合CSS选择器的节点。

parent = items.parents('.wrap')
print(parent)
运行结果：

<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
可以看到输出结果就少了一个节点，只保留了class为wrap的节点。

兄弟节点
在上面我们说明了子节点和父节点的用法，还有一种节点那就是兄弟节点，如果要获取兄弟节点可以使用siblings()方法。我们还是以上面的HTML代码为例来感受一下：

from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.list .item-0.active')
print(li.siblings())
在这里我们首先选择了class为list的节点内部的class为item-0和active的节点，也就是第三个li节点。那么很明显它的兄弟节点有四个，那就是第一、二、四、五个li节点。

运行结果：

<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0">first item</li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
可以看到运行结果也正是我们刚才所说的四个兄弟节点。

如果要筛选某个兄弟节点，我们依然可以向方法传入CSS选择器，这样就会从所有兄弟节点中挑选出符合条件的节点了。

from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.list .item-0.active')
print(li.siblings('.active'))
在这里我们筛选了class为active的节点，通过刚才的结果我们可以观察到class为active的兄弟节点只有第四个li节点，所以结果应该是一个。

运行结果：

<li class="item-1 active"><a href="link4.html">fourth item</a></li>
遍历
我们刚才可以观察到，PyQuery的选择结果可能是多个节点，可能是单个节点，类型都是PyQuery类型，并没有返回像BeautifulSoup一样的列表。

对于单个节点来说，我们可以直接打印输出，也可直接转成字符串。

from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
print(str(li))
运行结果：

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
对于多个节点的结果，我们就需要遍历来获取了，例如这里我们把每一个li节点进行遍历,，需要调用items()方法。

from pyquery import PyQuery as pq
doc = pq(html)
lis = doc('li').items()
print(type(lis))
for li in lis:
    print(li, type(li))
运行结果：

<class 'generator'>
<li class="item-0">first item</li>
<class 'pyquery.pyquery.PyQuery'>
<li class="item-1"><a href="link2.html">second item</a></li>
<class 'pyquery.pyquery.PyQuery'>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<class 'pyquery.pyquery.PyQuery'>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<class 'pyquery.pyquery.PyQuery'>
<li class="item-0"><a href="link5.html">fifth item</a></li>
<class 'pyquery.pyquery.PyQuery'>
在这里我们可以发现调用items()方法后，会得到一个生成器，遍历一下，就可以逐个得到li节点对象了，它的类型也是PyQuery类型，所以每个li标签还可以调用前面所说的方法进行选择，比如继续查询子节点，寻找某个祖先节点等等，非常灵活。

获取信息
提取到节点之后，我们的最终目的当然是提取节点所包含的信息了，比较重要的信息有两类，一是获取属性，二是获取文本，下面我们分别进行说明。

获取属性
提取到某个PyQuery类型的节点之后，我们可以调用attr()方法来获取属性。

html = '''
<div class="wrap">
<div id="container">
<ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
             <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
             <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')
print(a, type(a))
print(a.attr('href'))
运行结果：

<a href="link3.html"><span class="bold">third item</span></a> <class 'pyquery.pyquery.PyQuery'>
link3.html
``

在这里我们首先选中了class为item-0和active的li节点内的a节点，它的类型可以看到是PyQuery类型。

然后我们调用了attr()方法，然后传入属性的名称，就可以得到这个属性值了。

也可以通过调用attr属性来获取属性，用法如下：

```python
print(a.attr.href).md.blank.line.437.
结果：

link3.html
结果是完全一样的，在这里我们没有调用方法，而是调用了attr属性，然后再调用属性名，同样可以得到属性值。

如果我们选中的是多个元素，然后调用attr()方法会出现怎样的结果？我们用一个实例来测试一下。

a = doc('a')
print(a, type(a))
print(a.attr('href'))
print(a.attr.href)
运行结果：

<a href="link2.html">second item</a><a href="link3.html"><span class="bold">third item</span></a><a href="link4.html">fourth item</a><a href="link5.html">fifth item</a> <class 'pyquery.pyquery.PyQuery'>
link2.html
link2.html
照理来说我们选中的a节点应该有四个，而且打印结果也是四个，但是当我们调用attr()方法时，返回的结果却只是第一个。

所以当返回结果包含多个节点时，调用attr()方法只会得到第一个节点的属性。

那么遇到这种情况如果我们想获取所有的a节点的属性，就需要用到上文所说的遍历了。

from pyquery import PyQuery as pq
doc = pq(html)
a = doc('a')
for item in a.items():
    print(item.attr('href'))
运行结果：

link2.html
link3.html
link4.html
link5.html
所以，在进行属性获取的时候观察一下返回节点是一个还是多个，如果是多个，则需要遍历才能依次获取每个节点的属性。

获取文本
获取节点之后的另一个主要的操作就是获取其内部的文本了，我们可以调用text()方法来获取。

html = '''
<div class="wrap">
<div id="container">
<ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
             <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
             <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')
print(a)
print(a.text())
运行结果：

<a href="link3.html"><span class="bold">third item</span></a>
third item
我们首先选中了一个a节点，然后调用了text()方法，就可以获取其内部的文本信息了，它会忽略掉标签内部包含的所有HTML，只返回纯文字内容。

但如果我们想要获取这个节点内部的HTML文本，就可以用html()方法。

from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
print(li.html())
这里我们选中了第三个li节点，然后调用了html()方法，它返回的结果应该是li标签内的所有HTML文本。

运行结果：

<a href="link3.html"><span class="bold">third item</span></a>
这里同样有一个问题，如果我们选中的结果是多个节点，text()或html()会返回什么内容？

我们用一个实例来看一下：

html = '''
<div class="wrap">
<div id="container">
<ul class="list">
             <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
             <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
             <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('li')
print(li.html())
print(li.text())
print(type(li.text())
运行结果：

<a href="link2.html">second item</a>
second item third item fourth item fifth item
<class 'str'>
结果可能比较出乎意料，我们选中的是所有的li节点，可以发现html()方法返回的是第一个li节点的内部HTML文本，而text()则返回了所有的li节点内部纯文本，中间用一个空格分割开，实际上是一个字符串。

所以这个地方值得注意，如果我们得到的结果是多个节点，如果要获取每个节点的内部HTML文本，则需要遍历每个节点，而text()方法不需要遍历就可以获取，它是将所有节点取文本之后合并成一个字符串。

节点操作
PyQuery提供了一系列方法来对节点进行动态修改操作，比如为某个节点添加一个class，移除某个节点等等，这些操作有时候会为提取信息带来极大的便利。

由于节点操作的方法太多，下面举几个典型的例子来说明它的用法。

addClass、removeClass
我们先用一个实例来感受一下：

html = '''
<div class="wrap">
<div id="container">
<ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
             <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
             <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.removeClass('active')
print(li)
li.addClass('active')
print(li)
首先我们选中了第三个li节点，然后调用了removeClass()方法，将li的active这个class移除，后来又调用了addClass()方法，又将class添加回来，每执行一次操作，就打印输出一下当前li节点的内容。

运行结果：

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
可以看到一共进行了三次输出，第二次输出li标签的active这个class被移除了，第三次class又添加回来了。

所以说我们addClass()、removeClass()这些方法可以动态地改变节点的class属性。

attr、text、html


当然除了操作class这个属性，也有attr()方法来专门针对属性进行操作，也可以用text()、html()方法来改变节点内部的内容。

我们用实例感受一下：

html = '''
<ul class="list">
     <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
</ul>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.attr('name', 'link')
print(li)
li.text('changed item')
print(li)
li.html('<span>changed item</span>')
print(li)
在这里我们首先选中了li标签，然后调用attr()方法来修改属性，第一个参数为属性名，第二个参数为属性值，然后我们调用了text()和html()方法来改变节点内部的内容。三次操作后分别又打印输出当前li节点。

运行结果：

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0 active" name="link"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0 active" name="link">changed item</li>
<li class="item-0 active" name="link"><span>changed item</span></li>
可以发现，调用attr()方法后，li节点多来一个原本不存在的属性name，其值为link，调用text()方法，传入文本之后，发现li节点内部的文本就全被改变为传入的字符串文本了。调用html()方法传入HTML文本之后，li节点内部又改变为传入的HTML文本。

所以说，attr()方法如果只传入第一个参数属性名，则是获取这个属性值，如果传入第二个参数，可以用来修改属性值，text()和html()方法如果不传参数是获取节点内纯文本和HTML文本，如果传入参数则是进行赋值。

remove
remove顾名思义移除，remove()方法有时会为信息的提取带来非常大的便利。下面我们看一个实例：

html = '''
<div class="wrap">
    Hello, World
    <p>This is a paragraph.</p>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
wrap = doc('.wrap')
print(wrap.text())
在这里有一段HTML文本，我们现在想提取Hello, World这个字符串，而不要p节点内部的字符串，这个怎样来提取？

在这里我们直接先尝试提取class为wrap的节点的内容，看看是不是我们想要的，运行结果如下：

Hello, World This is a paragraph.
然而这个结果还包含了内部的p节点的内容，也就是说text()把所有的纯文本全提取出来了。如果我们想去掉p节点内部的文本，可以选择再把p节点内的文本提取一遍，然后从整个结果中移除这个子串，但这个做法明显比较繁琐。

那这是remove()方法就可以派上用场了，我们可以接着这么做:

wrap.find('p').remove()
print(wrap.text())
我们首先选中了p节点，然后调用了remove()方法将其移除，然后这时wrap内部就只剩下Hello, World这句话了，然后再利用text()方法提取即可。

所以说，remove()方法可以删除某些冗余内容，来方便我们的提取。在适当的时候使用可以极大地提高效率。

另外其实还有很多节点操作的方法，比如append()、empty()、prepend()等方法，他们和jQuery的用法是完全一致的，详细的用法可以看到官方文档。

http://pyquery.readthedocs.io/en/latest/api.html

伪类选择器
CSS选择器之所以强大，还有一个很重要的原因就是它支持多种多样的伪类选择器。例如选择第一个节点、最后一个节点、奇偶数节点、包含某一文本的节点等等，我们用一个实例感受一下：

html = '''
<div class="wrap">
<div id="container">
<ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="https://ask.hellobi.com/link2.html">second item</a></li>
             <li class="item-0 active"><a href="https://ask.hellobi.com/link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="https://ask.hellobi.com/link4.html">fourth item</a></li>
             <li class="item-0"><a href="https://ask.hellobi.com/link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('li:first-child')
print(li)
li = doc('li:last-child')
print(li)
li = doc('li:nth-child(2)')
print(li)
li = doc('li:gt(2)')
print(li)
li = doc('li:nth-child(2n)')
print(li)
li = doc('li:contains(second)')
print(li)
在这里我们使用了CSS3的伪类选择器，依次选择了第一个<li>节点、最后一个<li>节点、第二个<li>节点、第三个<li>之后的<li>节点、偶数位置的<li>节点、包含second文本的<li>节点，功能十分强大。

更多的CSS选择器的用法可以参照http://www.w3school.com.cn/css/index.asp

到此为止PyQuery的常用用法就介绍完了，如果想查看更多的内容可以参考一下PyQuery的官方文档http://pyquery.readthedocs.io，相信有了它，解析网页不再是难事。

