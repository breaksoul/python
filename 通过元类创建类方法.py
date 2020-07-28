class UpperAttrMetaClass(type):

    # __new__ 是在__init__之前被调用的特殊方法
    # __new__是用来创建对象并返回之的方法
    # 而__init__只是用来将传入的参数初始化给对象
    # 你很少用到__new__，除非你希望能够控制对象的创建
    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
    # 如果你希望的话，你也可以在__init__中做些事情
    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(cls, class_name, class_parents, class_attr):
        # 遍历属性字典，把不是__开头的属性名字变为大写
        new_attr = {}
        print("="*30)
        for name, value in class_attr.items():
            print("name=%s and value=%s" % (name,value))  # 打印所有类属性出来
            if not name.startswith("__"):
               new_attr[name.upper()] = value
               print("name.upper()=",name.upper())
               print("value=",value)
        
        # 调用type来创建一个类
        return type(class_name, class_parents, new_attr)

class Foo(object, metaclass=UpperAttrMetaClass):
    bar = 'bip'


print("="*30)
print("check Foo exist bar attr=",hasattr(Foo, 'bar'))
print("check Foo exist BAR attr=",hasattr(Foo, 'BAR'))

f = Foo()
print("print f.BAR=",f.BAR)









神级程序员通过两句话带你完全掌握Python最难知识点——元类！
千万不要被所谓“元类是99%的python程序员不会用到的特性”这类的说辞吓住。因为 每个中国人，都是天生的元类使用者

学懂元类，你只需要知道两句话：

道生一，一生二，二生三，三生万物

我是谁？我从哪来里？我要到哪里去？

在python世界，拥有一个永恒的道，那就是“type”，请记在脑海中，type就是道。如此广袤无垠的python生态圈，都是由type产生出来的。在给大家分享之前呢，小编推荐一下一个挺不错的交流宝地，里面都是一群热爱并在学习Python的小伙伴们，大几千了吧，各种各样的人群都有，特别喜欢看到这种大家一起交流解决难题的氛围，群资料也上传了好多，各种大牛解决小白的问题，这个Python群：330637182 欢迎大家进来一起交流讨论，一起进步，尽早掌握这门Python语言。

道生一，一生二，二生三，三生万物。

道即是 type

一即是 metaclass(元类，或者叫类生成器)

二即是 class(类，或者叫实例生成器)

三即是 instance(实例)

万物即是 实例的各种属性与方法，我们平常使用python时，调用的就是它们。

道和一，是我们今天讨论的命题，而二、三、和万物，则是我们常常使用的类、实例、属性和方法，用hello world来举例：

造物主，可以直接创造单个的人，但这是一件苦役。造物主会先创造“人”这一物种，再批量创造具体的个人。并将三大永恒命题，一直传递下去。

“道”可以直接生出“二”，但它会先生出“一”，再批量地制造“二”。

type可以直接生成类（class），但也可以先生成元类（metaclass），再使用元类批量定制类（class）。

元类——道生一，一生二

一般来说，元类均被命名后缀为Metalass。想象一下，我们需要一个可以自动打招呼的元类，它里面的类方法呢，有时需要say_Hello，有时需要say_Hi，有时又需要say_Sayolala，有时需要say_Nihao。

如果每个内置的say_xxx都需要在类里面声明一次，那将是多么可怕的苦役！ 不如使用 元类来解决问题。

以下是创建一个专门“打招呼”用的元类代码：

来！一起根据道生一、一生二、二生三、三生万物的准则，走进元类的生命周期吧！

注意：通过元类创建的类，第一个参数是父类，第二个参数是metaclass

普通人出生都不会说话，但有的人出生就会打招呼说“Hello”，“你好”,“sayolala”，这就是天赋的力量。它会给我们面向对象的编程省下无数的麻烦。

现在，保持元类不变，我们还可以继续创建Sayolala， Nihao类，如下：

太棒了！学到这里，你是不是已经体验到了造物主的乐趣？

python世界的一切，尽在掌握。

年轻的造物主，请随我一起开创新世界。

我们选择两个领域，一个是Django的核心思想，“Object Relational Mapping”，即对象-关系映射，简称ORM。

这是Django的一大难点，但学完了元类，一切变得清晰。你对Django的理解将更上一层楼！

另一个领域是爬虫领域（黑客领域），一个自动搜索网络上的可用代理，然后换着IP去突破别的人反爬虫限制。

这两项技能非常有用，也非常好玩！

挑战一：通过元类创建ORM

准备工作，创建一个Field类

它的作用是

在StringField,IntegerField实例初始化时，时自动调用父类的初始化方式。

道生一

它做了以下几件事

创建一个新的字典mapping

将每一个类的属性，通过.items()遍历其键值对。如果值是Field类，则打印键值，并将这一对键值绑定到mapping字典上。

将刚刚传入值为Field类的属性删除。

创建一个专门的__mappings__属性，保存字典mapping。

创建一个专门的__table__属性，保存传入的类的名称。

一生二

IntegerField(‘id’)就会自动解析为：

Model.__setattr__(self, ‘id’, IntegerField(‘id’))

因为IntergerField(‘id’)是Field的子类的实例，自动触发元类的__new__，所以将IntergerField(‘id’)存入__mappings__并删除这个键值对。

二生三、三生万物

当你初始化一个实例的时候并调用save()方法时候

u = User(id=12345, name='Batman', email='batman@nasa.org', password='iamback')u.save()

这时先完成了二生三的过程：

先调用Model.__setattr__，将键值载入私有对象

然后调用元类的“天赋”，ModelMetaclass.__new__，将Model中的私有对象，只要是Field的实例，都自动存入u.__mappings__。

接下来完成了三生万物的过程：

通过u.save()模拟数据库存入操作。这里我们仅仅做了一下遍历__mappings__操作，虚拟了sql并打印，在现实情况下是通过输入sql语句与数据库来运行。

这里，我们利用request包，把百度的源码爬了出来。

试一试抓百度

把这一段粘在get_page.py后面，试完删除

接下来进入正题：使用元类批量抓取代理

批量处理抓取代理

道生一：元类的__new__中，做了四件事：

将“crawl_”开头的类方法的名称推入ProxyGetter.__CrawlName__

将“crawl_”开头的类方法的本身推入ProxyGetter.__CrawlFunc__

计算符合“crawl_”开头的类方法个数

删除所有符合“crawl_”开头的类方法

怎么样？是不是和之前创建ORM的__mappings__过程极为相似？

一生二：类里面定义了使用pyquery抓取页面元素的方法

分别从三个免费代理网站抓取了页面上显示的全部代理。

如果对yield用法不熟悉，可以查看：

二生三：创建实例对象crawler

略

三生万物：遍历每一个__CrawlFunc__

在ProxyGetter.__CrawlName__上面，获取可以抓取的的网址名。

触发类方法ProxyGetter.get_raw_proxies(site)

遍历ProxyGetter.__CrawlFunc__,如果方法名和网址名称相同的，则执行这一个方法

把每个网址获取到的代理整合成数组输出。

那么。。。怎么利用批量代理，冲击别人的网站，套取别人的密码，狂发广告水贴，定时骚扰客户？ 呃！想啥呢！这些自己悟！如果悟不到，请听下回分解！

年轻的造物主，创造世界的工具已经在你手上，请你将它的威力发挥到极致！

请记住挥动工具的口诀：

道生一，一生二，二生三，三生万物

我是谁，我来自哪里，我要到哪里去

在理解元类之前，需要先掌握Python中的类，Python中类的概念与SmallTalk中类的概念相似。

在大多数语言中，类是用来描述如何创建对象的代码段，这在Python中也是成立的

Python那些事——何为元类？道生一，一生二，二生三，三生万物元

学懂元类，你只需要知道两句话：

道生一，一生二，二生三，三生万物

我是谁？我从哪来里？我要到哪里去？

在python世界，拥有一个永恒的道，那就是“type”，请记在脑海中，type就是道。如此广袤无垠的python生态圈，都是由type产生出来的。

道生一，一生二，二生三，三生万物。

道 即是 type

一 即是 metaclass(元类，或者叫类生成器)

二 即是 class(类，或者叫实例生成器)

三 即是 instance(实例)

万物 即是 实例的各种属性与方法，我们平常使用python时，调用的就是它们。

道和一，是我们今天讨论的命题，而二、三、和万物，则是我们常常使用的类、实例、属性和方法，用hello world来举例：

Python

1

2

3

4

5

6

7

8

9

10

11

创建一个Hello类，拥有属性say_hello ----二的起源
classHello():

defsay_hello(self,name='world'):

print('Hello, %s.'%name)

从Hello类创建一个实例hello ----二生三
hello=Hello()

使用hello调用方法say_hello ----三生万物
hello.say_hello()

输出效果：

Hello,world.

这就是一个标准的“二生三，三生万物”过程。 从类到我们可以调用的方法，用了这两步。

那我们不由自主要问，类从何而来呢？回到代码的第一行。

class Hello其实是一个函数的“语义化简称”，只为了让代码更浅显易懂，它的另一个写法是：

deffn(self,name='world'):# 假如我们有一个函数叫fn

Hello=type('Hello',(object,),dict(say_hello=fn))# 通过type创建Hello class ---- 神秘的“道”，可以点化一切，这次我们直接从“道”生出了“二”

这样的写法，就和之前的Class Hello写法作用完全相同，你可以试试创建实例并调用

从Hello类创建一个实例hello ----二生三，完全一样
使用hello调用方法say_hello ----三生万物，完全一样
Hello,world.----调用结果完全一样。

我们回头看一眼最精彩的地方，道直接生出了二：

Hello = type(‘Hello’, (object,), dict(say_hello=fn))

这就是“道”，python世界的起源，你可以为此而惊叹。

注意它的三个参数！暗合人类的三大永恒命题：我是谁，我从哪里来，我要到哪里去。

第一个参数：我是谁。 在这里，我需要一个区分于其它一切的命名，以上的实例将我命名为“Hello”

第二个参数：我从哪里来

在这里，我需要知道从哪里来，也就是我的“父类”，以上实例中我的父类是“object”——python中一种非常初级的类。

第三个参数：我要到哪里去

在这里，我们将需要调用的方法和属性包含到一个字典里，再作为参数传入。以上实例中，我们有一个say_hello方法包装进了字典中。

值得注意的是，三大永恒命题，是一切类，一切实例，甚至一切实例属性与方法都具有的。理所应当，它们的“创造者”，道和一，即type和元类，也具有这三个参数。但平常，类的三大永恒命题并不作为参数传入，而是以如下方式传入

classHello(object){

class 后声明“我是谁”
小括号内声明“我来自哪里”
中括号内声明“我要到哪里去”
defsay_hello(){

}

造物主，可以直接创造单个的人，但这是一件苦役。造物主会先创造“人”这一物种，再批量创造具体的个人。并将三大永恒命题，一直传递下去。

“道”可以直接生出“二”，但它会先生出“一”，再批量地制造“二”。

type可以直接生成类（class），但也可以先生成元类（metaclass），再使用元类批量定制类（class）。

元类——道生一，一生二

一般来说，元类均被命名后缀为Metalass。想象一下，我们需要一个可以自动打招呼的元类，它里面的类方法呢，有时需要say_Hello，有时需要say_Hi，有时又需要say_Sayolala，有时需要say_Nihao。

如果每个内置的say_xxx都需要在类里面声明一次，那将是多么可怕的苦役！ 不如使用元类来解决问题。

以下是创建一个专门“打招呼”用的元类代码：

classSayMetaClass(type):

def__new__(cls,name,bases,attrs):

attrs['say_'+name]=lambdaself,value,saying=name:print(saying+','+value+'!')

returntype.__new__(cls,name,bases,attrs)

记住两点：

1、元类是由“type”衍生而出，所以父类需要传入type。【道生一，所以一必须包含道】

2、元类的操作都在 __new__中完成，它的第一个参数是将创建的类，之后的参数即是三大永恒命题：我是谁，我从哪里来，我将到哪里去。 它返回的对象也是三大永恒命题，接下来，这三个参数将一直陪伴我们。

在__new__中，我只进行了一个操作，就是

它跟据类的名字，创建了一个类方法。比如我们由元类创建的类叫“Hello”，那创建时就自动有了一个叫“say_Hello”的类方法，然后又将类的名字“Hello”作为默认参数saying，传到了方法里面。然后把hello方法调用时的传参作为value传进去，最终打印出来。

那么，一个元类是怎么从创建到调用的呢？

来！一起根据道生一、一生二、二生三、三生万物的准则，走进元类的生命周期吧！

12

13

14

15

16

17

18

19

道生一：传入type
传入三大永恒命题：类名称、父类、属性
创造“天赋”
传承三大永恒命题：类名称、父类、属性
一生二：创建类
classHello(object,metaclass=SayMetaClass):

pass

二生三：创建实列
三生万物：调用实例方法
hello.say_Hello('world!')

输出为

Hello,world!

注意：通过元类创建的类，第一个参数是父类，第二个参数是metaclass

普通人出生都不会说话，但有的人出生就会打招呼说“Hello”，“你好”,“sayolala”，这就是天赋的力量。它会给我们面向对象的编程省下无数的麻烦。

现在，保持元类不变，我们还可以继续创建Sayolala， Nihao类，如下：

classSayolala(object,metaclass=SayMetaClass):

s=Sayolala()

s.say_Sayolala('japan!')

输出

Sayolala,japan!

也可以说中文

classNihao(object,metaclass=SayMetaClass):

n=Nihao()

n.say_Nihao('中华!')

Nihao,中华!

再来一个小例子：

道生一
classListMetaclass(type):

天赋：通过add方法将值绑定
attrs['add']=lambdaself,value:self.append(value)

一生二
classMyList(list,metaclass=ListMetaclass):

二生三
L=MyList()

三生万物
L.add(1)

现在我们打印一下L

print(L)

[1]

而普通的list没有add()方法

L2=list()

L2.add(1)

AttributeError:'list'objecthas no attribute'add'

太棒了！学到这里，你是不是已经体验到了造物主的乐趣？

python世界的一切，尽在掌握。

年轻的造物主，请随我一起开创新世界。

我们选择两个领域，一个是Django的核心思想，“Object Relational Mapping”，即对象-关系映射，简称ORM。

这是Django的一大难点，但学完了元类，一切变得清晰。你对Django的理解将更上一层楼！

另一个领域是爬虫领域（黑客领域），一个自动搜索网络上的可用代理，然后换着IP去突破别的人反爬虫限制。

这两项技能非常有用，也非常好玩！

挑战一：通过元类创建ORM

准备工作，创建一个Field类

classField(object):

def__init__(self,name,column_type):

self.name=name

self.column_type=column_type

def__str__(self):

return'<%s:%s>'%(self.__class__.__name__,self.name)

它的作用是

在Field类实例化时将得到两个参数，name和column_type，它们将被绑定为Field的私有属性，如果要将Field转化为字符串时，将返回“Field:XXX” ， XXX是传入的name名称。

准备工作：创建StringField和IntergerField

classStringField(Field):

def__init__(self,name):

super(StringField,self).__init__(name,'varchar(100)')

classIntegerField(Field):

super(IntegerField,self).__init__(name,'bigint')

在StringField,IntegerField实例初始化时，时自动调用父类的初始化方式。

道生一

classModelMetaclass(type):

ifname=='Model':

print('Found model: %s'%name)

mappings=dict()

fork,vinattrs.items():

ifisinstance(v,Field):

print('Found mapping: %s ==> %s'%(k,v))

mappings[k]=v

forkinmappings.keys():

attrs.pop(k)

attrs['mappings']=mappings# 保存属性和列的映射关系

attrs['table']=name# 假设表名和类名一致

它做了以下几件事

创建一个新的字典mapping

将每一个类的属性，通过.items()遍历其键值对。如果值是Field类，则打印键值，并将这一对键值绑定到mapping字典上。

将刚刚传入值为Field类的属性删除。

创建一个专门的__mappings__属性，保存字典mapping。

创建一个专门的__table__属性，保存传入的类的名称。

一生二

20

21

22

23

24

classModel(dict,metaclass=ModelMetaclass):

def__init__(self,**kwarg):

super(Model,self).__init__(**kwarg)

def__getattr__(self,key):

try:

returnself[key]

exceptKeyError:

raiseAttributeError("'Model' object has no attribute '%s'"%key)

def__setattr__(self,key,value):

self[key]=value

模拟建表操作
defsave(self):

fields=[]

args=[]

fork,vinself.__mappings__.items():

fields.append(v.name)

args.append(getattr(self,k,None))

sql='insert into %s (%s) values (%s)'%(self.__table__,','.join(fields),','.join([str(i)foriinargs]))

print('SQL: %s'%sql)

print('ARGS: %s'%str(args))

如果从Model创建一个子类User：

classUser(Model):

定义类的属性到列的映射：
id=IntegerField('id')

name=StringField('username')

email=StringField('email')

password=StringField('password')

这时

id= IntegerField(‘id’)就会自动解析为：

Model.__setattr__(self, ‘id’, IntegerField(‘id’))

因为IntergerField(‘id’)是Field的子类的实例，自动触发元类的__new__，所以将IntergerField(‘id’)存入__mappings__并删除这个键值对。

二生三、三生万物

当你初始化一个实例的时候并调用save()方法时候

u=User(id=12345,name='Batman',email='batman@nasa.org',password='iamback')

u.save()

这时先完成了二生三的过程：

先调用Model.__setattr__，将键值载入私有对象

然后调用元类的“天赋”，ModelMetaclass.__new__，将Model中的私有对象，只要是Field的实例，都自动存入u.__mappings__。

接下来完成了三生万物的过程：

通过u.save()模拟数据库存入操作。这里我们仅仅做了一下遍历__mappings__操作，虚拟了sql并打印，在现实情况下是通过输入sql语句与数据库来运行。

输出结果为

Found model:User

Found mapping:name==>

Found mapping:password==>

Found mapping:id==>

Found mapping:email==>

SQL:insert into User(username,password,id,email)values(Batman,iamback,12345,batman@nasa.org)

ARGS:['Batman','iamback',12345,'batman@nasa.org']

年轻的造物主，你已经和我一起体验了由“道”演化“万物”的伟大历程，这也是Django中的Model版块核心原理。

接下来，请和我一起进行更好玩的爬虫实战（嗯，你现在已经是初级黑客了）：网络代理的爬取吧！

挑战二：网络代理的爬取

准备工作，先爬个页面玩玩

请确保已安装requests和pyquery这两个包。

文件：get_page.py
importrequests

base_headers={

'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',

'Accept-Encoding':'gzip, deflate, sdch',

'Accept-Language':'zh-CN,zh;q=0.8'

defget_page(url):

headers=dict(base_headers)

print('Getting',url)

r=requests.get(url,headers=headers)

print('Getting result',url,r.status_code)

ifr.status_code==200:

returnr.text

exceptConnectionError:

print('Crawling Failed',url)

returnNone

这里，我们利用request包，把百度的源码爬了出来。

试一试抓百度

把这一段粘在get_page.py后面，试完删除

if(name=='main'):

rs=get_page('https://www.baidu.com')

print('result:\r\n',rs)

试一试抓代理

frompyquery importPyQuery aspq

start_url='//www.proxy360.cn/Region/China'

print('Crawling',start_url)

html=get_page(start_url)

ifhtml:

doc=pq(html)

lines=doc('div[name="list_proxy_ip"]').items()

forline inlines:

ip=line.find('.tbBottomLine:nth-child(1)').text()

port=line.find('.tbBottomLine:nth-child(2)').text()

print(ip+':'+port)

接下来进入正题：使用元类批量抓取代理

批量处理抓取代理

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

fromgetpage importget_page

道生一：创建抽取代理的metaclass
classProxyMetaclass(type):

"""

元类，在FreeProxyGetter类中加入

__CrawlFunc__和CrawlFuncCount

两个参数，分别表示爬虫函数，和爬虫函数的数量。

count=0

attrs['CrawlFunc']=[]

attrs['CrawlName']=[]

if'crawl_'ink:

attrs['CrawlName'].append(k)

attrs['CrawlFunc'].append(v)

count+=1

forkinattrs['CrawlName']:

attrs['CrawlFuncCount']=count

一生二：创建代理获取类
classProxyGetter(object,metaclass=ProxyMetaclass):

defget_raw_proxies(self,site):

proxies=[]

print('Site',site)

forfunc inself.__CrawlFunc__:

iffunc.__name__==site:

this_page_proxies=func(self)

forproxy inthis_page_proxies:

print('Getting',proxy,'from',site)

proxies.append(proxy)

returnproxies

defcrawl_daili66(self,page_count=4):

start_url='//www.66ip.cn/{}.html'

urls=[start_url.format(page)forpage inrange(1,page_count+1)]

forurl inurls:

print('Crawling',url)

html=get_page(url)

trs=doc('.containerbox table tr:gt(0)').items()

fortr intrs:

ip=tr.find('td:nth-child(1)').text()

port=tr.find('td:nth-child(2)').text()

yield':'.join([ip,port])

defcrawl_proxy360(self):

defcrawl_goubanjia(self):

start_url='//www.goubanjia.com/free/gngn/index.shtml'

tds=doc('td.ip').items()

fortd intds:

td.find('p').remove()

yieldtd.text().replace(' ','')

if__name__=='main':

二生三：实例化ProxyGetter
crawler=ProxyGetter()

print(crawler.__CrawlName__)

forsite_label inrange(crawler.__CrawlFuncCount__):

site=crawler.__CrawlName__[site_label]

myProxies=crawler.get_raw_proxies(site)

道生一：元类的__new__中，做了四件事：

将“crawl_”开头的类方法的名称推入ProxyGetter.__CrawlName__

将“crawl_”开头的类方法的本身推入ProxyGetter.__CrawlFunc__

计算符合“crawl_”开头的类方法个数

删除所有符合“crawl_”开头的类方法

怎么样？是不是和之前创建ORM的__mappings__过程极为相似？

一生二：类里面定义了使用pyquery抓取页面元素的方法

分别从三个免费代理网站抓取了页面上显示的全部代理。

如果对yield用法不熟悉，可以查看：

廖雪峰的python教程：生成器

二生三：创建实例对象crawler

略

三生万物：遍历每一个__CrawlFunc__

在ProxyGetter.__CrawlName__上面，获取可以抓取的的网址名。

触发类方法ProxyGetter.get_raw_proxies(site)

遍历ProxyGetter.__CrawlFunc__,如果方法名和网址名称相同的，则执行这一个方法

把每个网址获取到的代理整合成数组输出。

那么。。。怎么利用批量代理，冲击别人的网站，套取别人的密码，狂发广告水贴，定时骚扰客户？ 呃！想啥呢！这些自己悟！如果悟不到，请听下回分解！

年轻的造物主，创造世界的工具已经在你手上，请你将它的威力发挥到极致！

如果有来生，一个人去远行，看不同的风景，感受生命的活力。。。