小猫，第二周任务新鲜出炉了。

# ch1任务

在命令行下实现一个本地查询城市天气的程序

城市天气数据来自本地一个文件
<!-- more -->
然后，至少要有以下4个功能

- 输入help，获取帮助信息

- 输入quit，退出程序

- 输入history，显示历史查询信息

- 输入城市名，获得该城市天气状况



看到这里，估计你应该有个大概的框架了，这个程序

- 需要与用户交互，判断用户输入的内容，执行相应的操作

- 需要提取天气数据放到内存中，方便程序进行快速查找

- 需要根据用户输入的城市名，找到对应的天气状况

- 需要保存历史查询信息




首先，

# 与用户交互

咱们现在这个阶段学得一个方法是通过input函数来等待用户输入，并将返回值赋值给一个变量

> userInput = input("输入一个城市名：")

现在，userInput里面就保存了，用户输入的内容

要判断这个内容是什么，首先得查一下input函数的文档，它的返回值是什么类型，知道了返回值类型，我们才好使用相同的类型去与它进行对比

那就先查[文档](https://docs.python.org/3/library/functions.html?highlight=input#input)呗，

> The function then reads a line from input, converts it to a string (stripping a trailing newline), and returns that.

从这句话中可以知道，input返回的是string(字符串)，所以咱们就可以使用字符串来与input的返回值进行对比了

如何对比呢？

当然是使用python的比较运算符了，就像做加法一样，得用加号

python的比较运算符有 >、 <、 <=、 >=、 ==、 !=，比较两个东西是不是相等，那就是'=='它了。

> userInput == 'quit'
>
> userInput == 'help'
>
> userInput == 'history'

光这样写个表达式出来，好像意义不大，关键是咱们要根据这个表达式的值来控制程序的流程走向

所以，小猫，你应该很快可以想到使用if语句了吧。像这样


> if userInput == 'quit':
>
>   ...
>
> elif userInput == 'help':
>
>   ...
>
> elif userInput == 'history':
>
>   ...
>
> else:
>
>    ...


好，获取用户输入进行判断的问题基本有方案了，对吧，那现在咱们开始研究第二个问题

# 提取天气数据到内存中

因为在这个任务中，天气数据是保存在本地文件的，所以要提取这个数据，咱们需要先打开它

打开文件当然是使用open方法

光知道方法名还不够全面，万一它还要带必须的参数呢？然后它的返回值又是什么呢？所以如果你不熟悉它的用法的话，还得先去[官方文档](https://docs.python.org/3/library/functions.html?highlight=open#open)中查一下

> open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
>
> Open file and return a corresponding file object. If the file cannot be opened, an OSError is raised.
>

可以看到，open函数的参数还是蛮多的

在文档中，有每个参数的详细解释，你自己可以尝试去读读，而且还提供了栗子

> file参数是文件路径

> mode参数是读写模式，比如你是只要读取文件内容呢？还是要进行内容修改？只是读取的话，那就好简单了，使用'r'就可以，这个参数在有多种类型，而且可以进行模式组合，比如，默认情况下是'rt'，你可以自己修改它为'rb'、'wb'等等

最常用的就是这两个参数了，其中file是必须要提供的参数，其他都是可选的

也就是说，你可以这样写

> open('test.txt')

也可以这样写

> open('test.txt','rt')


ok,文件可以打开了，那接下来就是读出文件内容

打开文件用了open方法，读文件会不会是read方法呢？在《笨办法学Python》中也有用到这个方法，不记得的话，回去再翻翻

> f = open('test.txt','rt')
>
> f.read()
>

现在，文件打开了，内容也读出来了，那就将内容放到内存中去呗

要把它放到内存中，只要用一个变量来接收这个内容就可以了

像这样

> weatherTxt = f.read()

现在回忆一下，变量是什么？变量有哪些类型？

你可以把变量想象成一个收纳箱的名字，这个收纳箱放在内存里边，可以装东西进去，你需要使用这个收纳箱里边的东西时，只要跟电脑说出这个收纳箱的名字(变量)，它就会把收纳箱里边的东西放到你面前

每个收纳箱可能装的东西会不一样，有字符串，有数字，有列表型的箱子，有字典型的箱子。。。

收纳箱真是个好东西，你觉得看不顺眼的，杂七杂八的东西都可以往里边装，要取出它的时候，呼唤它的名就欧了。

在这个任务中，咱们使用什么类型的收纳箱来装天气数据呢？

这就得分析文件中的天气数据了

> 这里的天气数据是没有先后顺序的
>
> 每个城市名是不一样的，但是相应的天气状况各个城市之间可以一样
>
> 每个城市名都对应一种天气状况

对比python中的数据类型后，有没有觉得字典的特性非常的符合这种天气数据的特点

没错，就用字典箱了装天气数据，像这样

> d['北京'] = ‘雾霾’
>
> d['广州'] = '高温'
>
> d['上海'] = '小雨'

上面的d就是一个字典箱子的名字，就这样往里边装东西

现在这个箱子里边装了这么几个玩意儿

{'北京':'雾霾', '广州':'高温', '上海':'小雨'}


接下来，关键功能来了

# 根据城市名来找到天气状况

刚才已经说了，天气数据被咱们装在一个名叫d的字典箱子里边

现在需要从箱子里边拿出来

从字典箱子里边取数据，就跟查字典似的

在目录中根据拼音找到相应的汉字

这个箱子里边，城市名对应拼音，天气对应汉字

所以，想要知道某个城市的天气，首先得知道这个城市的名字

> d['广州']

像上面这样，就可以找到广州的天气了。

太棒了，关键功能这么简单就实现了，多亏了这个字典箱子。

根据任务，还需要

# 返回历史查询信息

当输入'history'时，显示用户查询过的城市天气信息

那也就是说，在刚才从字典箱子里边取天气数据后，需要把这次查询记录保存到另一个箱子中，以便用户能够提取这些历史记录

看，又是一个保存数据的问题，那肯定也是用个箱子来装咯

这时用什么类型的箱子比较好呢？

小猫，以你现在的python知识，肯定知道python中常见的箱子有列表箱、字典箱、元组箱

> 说到历史，都是有发生时间的，所以很明显，历史是有顺序的，这个历史数据有点列表的痕迹
>
> 当前程序的天气数据是一个城市名对应一个天气状况，这个特性可以用二元元组来表示
>

那如何既让历史数据既有顺序又成对出现？

所以，天气历史数据可以用一个装有二元元组的列表箱子来保存，假设这个箱子的名字叫weatherList

类似

> [('北京','雾霾'),('广州','高温'),('上海','小雨')]

这样在装入历史数据时，可以使用列表的append方法将每次查询添加到列表箱子的末尾

> weatherList.append(tuple(('北京','雾霾')))
> weatherList.append(tuple(('广州','高温')))
> weatherList.append(tuple(('上海','小雨')))

读取数据时，可以使用循环根据历史查询顺序取出

> for wl in weatherList:
>
>   print(wl[0],wl[1])


wl是列表箱子中的一个元素，这个元素是一个二元元组，元组的第一个元素wl[0]保存的城市名,元组的第二个元素wl[1]保存的是天气状况

保存天气数据是一个字典箱子，保存历史查询记录是一个二元元组列表箱子，存取这个两个箱子中的动作，构成了这个任务的关键步骤

python中有各种各样有用的箱子，python程序说到底也就是倒腾这些箱子，所以熟悉这些箱子的特性和应用场景还是蛮重要的


小猫，为实现这个天气查询程序所需的4个主要功能都实现了，码码去吧。

# v1.0


```
def getWeatherData(): # 获取天气数据
	wd = {}
	with open(wPath,'r') as wf:
		for f in wf:
			wd[f.split(",")[0].strip()] = f.split(",")[1].strip()
	return wd

def getHelp(): # 获取帮助信息
	print(helpInfo)

def setHistory(city,weatherStatus):
	historyList.append(tuple((city,weatherStatus))) #将城市名和天气状况转换成元组元素放入列表箱子中

def getHistory(): # 获取历史查询信息
	if len(historyList) == 0: print("没有历史查询信息")
	for history in historyList:
		print(history[0],history[1]) # 访问列表箱子中的元组元素

def getCityWeather(info,weatherData): # 查询天气信息
	print("%s 的天气状况是： %s" % (info,weatherData[info]))
	setHistory(info,weatherData[info])

def exitApp(): # 退出程序
	exit(0)

def getInput(): # 获得用户输入信息
	userInput = input("输入一个城市名查询当地天气: ")
	return userInput

def go(weatherData): # 递归判断用户输入信息
	info = getInput()
	if info == 'quit':
		exitApp()
	elif info == 'help':
		getHelp()
		go(weatherData)
	elif info == 'history':
		getHistory()
		go(weatherData)
	elif info in weatherData.keys():
		getCityWeather(info,weatherData)
		go(weatherData)
	else:
		print("对不起，没有找到相关信息，可输入help获得帮助")
		go(weatherData)

if __name__ == '__main__':
	wPath = "/home/damao/project/Py103/Chap1/project/weather_info.txt"
	helpInfo = """
	输入 城市名，查询该城市的天气；
	输入 help，获取帮助文档；
	输入 history，获取查询历史；
	输入 quit，退出天气查询系统。
	"""
	historyList = []
	wDict = getWeatherData()
	go(wDict)


```
# 优化

小猫，咱们来继续优化任务代码

至少可以从以下方面进行优化

- 获得输入时，去掉两边空格
- 增加中文输入判断
- while不定次循环替代递归调用
- 给历史查询信息增加日期时间


## ch1任务模型

查询天气程序的模型是下面这个go函数

它获取用户输入后，判断输入内容执行相应的流程

如，输入内容为quit时，程序退出；输入内容为help时，展现帮助文档


```
weatherData = {'北京':'雾霾', '广州':'高温', '上海':'小雨'}

def go(weatherData): # 递归判断用户输入信息

	info = getInput()

	if info == 'quit':
		print("退出程序")

	elif info == 'help':
		print("显示帮助信息")
		go(weatherData)

	elif info == 'history':
		print("显示历史查询信息")
		go(weatherData)

	elif info in weatherData.keys():
		print("显示城市天气状况")
		go(weatherData)

	else:
		print("没有找到相关信息，可输入help获得帮助")
		go(weatherData)

```

## 去掉空格并转换成大写

不区分大小写使得用户输入可以更加灵活，在获取用户输入时去掉两边空格后转换成大写，并与大写关键字进行对比

> info = input("输入：").strip().upper()
>
> if info == 'Q' or info == 'QUIT':
>
> ......

## 增加中文判断，减少切换输入法

用户在输入城市名时使用的是中文输入法，为退出、历史、帮助功能增加中文输入判断，使得用户在各种输入过程中可以不进行输入法切换


> if info == '退出':
>
>		......
>
> elif info == '帮助':
>
>		......
>
> elif info == '历史':
>
> 	......
>
> else:
>
> 	......


## while循环代替递归调用

while循环可用于不定次数的循环场景，更适合这个天气查询程序，直至用户输入q或quit时，才退出循环

> while True:
>
> 	.......


所以，执行以上3个优化后，ch1任务模型如下

```
weatherData = {'北京':'雾霾', '广州':'高温', '上海':'小雨'}

def go(weatherData):

	while True:
		info = input("输入：").strip().upper()

		if info == 'Q' or info == 'QUIT' or info == '退出':
			print("退出程序")

		elif info == 'H' or info == 'HELP' or info == '帮助':
			print('显示帮助信息')

		elif info == 'HISTORY' or info == '历史':
			print('显示历史查询信息')

		elif info in weatherData.keys():
			print('显示城市天气状况')

		else:
			print("没有找到相关信息，可输入h或help获得帮助")
```

代码行数更少了，并且更加清晰易读


## 为历史信息增加日期时间

为了记录每次查询天气的时间点，在保存城市名和天气状况信息的同时也保存日期时间信息

python中time和datetime模块提供了日期时间相关的操作方法

如，datetime.datetime.now()用于提取当前系统时间，该函数返回一个datetime对象，可以一次提取年月日，时分秒

> dtn =datetime.datetime.now()
>
> year = dtn.year
>
> month = dtn.month
>
> day = dtn.day
>
> hour = dtn.hour
>
> minute = dtn.minute
>
> second = dtn.second

也可使用strftime函数格式化datetime对象，可按用户设定的格式输出时间

> In [1]: import datetime
>
> In [2]: dtn = datetime.datetime.now()
>
> In [3]: s = dtn.strftime('%Y-%m-%d %H:%M:%S')
>
> In [4]: print(s)
>
> 2017-01-11 20:53:18

各个优化完成，出优化后版本

# v1.1

```
import datetime
def getWeatherData(): # 获取天气数据
	wd = {}
	with open(wPath,'r') as wf:
		for f in wf:
			wd[f.split(",")[0].strip()] = f.split(",")[1].strip()
	return wd

def getHelp(): # 获取帮助信息
	global helpInfo
	print(helpInfo)

def setHistory(city,weatherStatus): # 保存历史查询记录
	#加入序号，时间，城市名，天气状况
	global historyList
	no = len(historyList)#获取列表长度
	dtn = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	historyList.append(tuple((no + 1,dtn,city,weatherStatus))) #转换成4元元组

def getHistory(): # 获取历史查询信息
	global historyList
	if len(historyList) == 0: print("没有历史查询信息")
	for history in historyList:
		print(history[0],history[1],history[2],history[3]) # 访问元组

def getCityWeather(info,weatherData): # 查询天气信息
	print("%s 的天气状况是： %s" % (info,weatherData[info]))
	setHistory(info,weatherData[info])

def exitApp(): # 退出程序
	exitCode = 0
	getHistory()
	exit(exitCode)

def getInput(): # 获得用户输入信息
	userInput = input("输入一个城市名查询当地天气: ")
	return userInput

def go(weatherData): # 判断用户输入信息
	while True:
		info = getInput().strip().upper()
		if info == 'Q' or info == 'QUIT' or info == '退出':
			exitApp()
		elif info == 'H' or info == 'HELP' or info == '帮助':
			getHelp()
		elif info == 'HISTORY' or info == '历史':
			getHistory()
		elif info in weatherData.keys():
			getCityWeather(info,weatherData)
		else:
			print("没有找到相关信息，可输入h或help获得帮助")

if __name__ == '__main__':
	wPath = "/home/damao/project/Py103/Chap1/project/weather_info.txt"
	helpInfo = """
	输入 城市名，查询该城市的天气；
	输入 h或help或帮助，获取帮助文档；
	输入 history或历史，获取查询历史；
	输入 q或quit或退出，退出天气查询系统。
	"""
	historyList = []
	wDict = getWeatherData()
	go(wDict)

```
