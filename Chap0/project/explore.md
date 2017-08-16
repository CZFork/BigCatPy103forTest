
**自主探索的最佳姿势，不是沿知识树学习，而是解决问题。**

## 需求

在本次课程中，我想将笔记推送到课程仓库的同时也发布在个人博客网站上。

所以一般情况下，流程是这样的：
<!-- more -->
1. 在课程仓库中写笔记

1. 在博客仓库中新建一个文件

1. 将笔记内容复制到博客仓库中新建的文件里边

1. 为新建的博客文件增加front-matter,以便HEXO可以识别标题并开启评论功能

1. 打开终端

1. 进入课程仓库目录

1. 执行3个git命令，推送到github

1. 进入博客仓库目录

1. 执行2个hexo命令，推送博客文章到github上的博客仓库

需要执行9个步骤来完成课程笔记和博客网站的内容更新。

作为一个惰星人，想要用python来自动化这个过程。

------

## 实现过程

### version 1.2

这次重新整理了下课程目录结构，project目录下的README.md改成了explore.md，用来记录自主的探索过程。note目录里边的README.md用来记录课程任务笔记。

![现在的课程目录结构图](http://7xrtxq.com1.z0.glb.clouddn.com/course_dir.png)

上一版本中，还有几个问题没有解决。

#### 第一个问题

获取需要更新的章节号时，判断用户输入是否为数字的问题

![获取章节号效果图](http://7xrtxq.com1.z0.glb.clouddn.com/getchapternumber.png)

python3中，input函数用来与用户交互，获得用户输入，并以string形式返回，由于博客文章标题是根据章节号来生成，并且这次课程总共有10个章节，所以这里需要用户输入一个范围在0到9之间的数字，若不是在这范围内的数字则提示用户并继续提供交互输入

所里这里就需要判断用户输入的是不是0到9之间的1个数字

- 判断是不是数字有以下几种方法

	1. str.isdecimal()方法

	1. 正则表达式

- 判断数字范围是不是在0到9之间也有几种办法

	1. 生成一个0到9的数字列表，判断数字是不是在这个列表里边

	1. 数字是否大于等于0并且小于等于9, 0 <= x <= 9

	1. 正则表达式

似乎正则表达式是比较好的选择，两个判断一步完成。

搜索正则表达式[资料](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832260566c26442c671fa489ebc6fe85badda25cd000)

python中有一个模块[re](https://docs.python.org/3/library/re.html?highlight=re#module-re)来提供正则表达式的相关操作，如re.match(pattern, string, flags=0)方法可以判断字符串是否与正则表达式匹配，匹配返回一个Match对象，否则返回None。

match函数有3个参数，第一个是正则表达式；第二个是要匹配的字符串；第三个是我翻译成条件标识，可以让match忽略大小写、多行匹配等

判断一个0到9之间的数字，用正则表达式来表达，一开始想当然的认为是[0-9]，测试时发现大于9的整数和小数也匹配了。

改成`^[0-9]$`后，匹配结果符合预期。[参考](https://zh.wikipedia.org/wiki/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F)

> ^	匹配输入字符串的开始位置
> 
> $	匹配输入字符串的结束位置


为了省掉转义字符的烦恼，正则表达式以字母前缀`r`开头，r'^[0-9]$'。

所以判断用户输入是否是一个0-9之间的数字可以这样

```
# test.py

import re
s = input("Input a number: ")
isNumber = r'^[0-9]$'
m = re.match(isNumber,s)
if m:
	print("It's a number.")
else:
	print("Not a number.")
```
![执行结果](http://7xrtxq.com1.z0.glb.clouddn.com/re.png)


#### 第二个问题

异常处理，捕捉各种异常，不至于在打开一个不存在的文件时，直接崩溃退出，不友好

这里主要处理open函数可能出现的异常

使用try来捕获异常

try:
	...
except 异常名:
	...
else:

```
# test.py

try:
	f = open('test.txt','r')
except IOError:
	print("No such a file")
else:
	print(f.read())
	f.close()
```


#### 第三个问题

提供正常退出机制，如获取到用户输入字母q或单词quit(不区分大小写)时，退出程序

```
# test.py

s = input("What can i do for you ? (q or quit for exit) ")
if s.upper() == 'QUIT' or s.upper() == 'Q':
	exit(0)
print("After ...")
```

执行时，不管输入大小写q或quit都正常退出程序。



上面3个问题的处理方案结合之前的代码

#### V1.2代码


```
import subprocess
import tempfile
import shutil
import re

def welcome(): # print welcome information
	welcomeWords = """
 		+---+---+---+---+---+---+---+
 		| W | E | L | C | O | M | E |
 		+---+---+---+---+---+---+---+
	"""
	print(welcomeWords)
	print("\n")
	print("Which chapter do you want to update? (q or quit for exit)")
	userInput = input("Input a chapter number (eg.0,1,2,3...9): ")
	if userInput.upper() == 'Q' or userInput.upper() == 'QUIT':
		exit(0)
	elif re.match(reExpression,userInput):
		return int(userInput)
	else:
		print("\n")
		print("Please input an integer number")
		return welcome()

def doSomething(): # do what
	doWhat = [
	"1.Git to Py103",
	"2.Note ---> Temp ---> Hexo",
	"3.Explore ---> Temp ---> Hexo",
	"4.Hexo to Blog"
	]

	for do in doWhat:
		print(do)
	what = input("What can i do for you? (eg. 1,2,3,4) ")
	if what.upper() == 'Q' or what.upper() == 'QUIT':
		exit(0)
	elif re.match(reExpression,what):
			if what == '1':
				return 1
			elif what == '2':
				return 2
			elif what == '3':
				return 3
			elif what == '4':
				return 4
			else:
				return -1
	else:
		print("\n")
		print("Please input an integer number")
		return doSomething()

def go(): # welcome and do something
	iDo = doSomething()
	if iDo == 1:
		r = gitCmd(gitDir)
		go()
	elif iDo == 2:
		tfp = note2temp(notePath,frontMatter)
		r = temp2hexo(tfp,hexoNotePath)
		if r == 0:
			go()
	elif iDo == 3:
		tfp = explore2temp(projectPath,expFrontMatter)
		r = temp2hexo(tfp,hexoExpPath)
		if r == 0:
			go()
	elif iDo == 4:
		r = hexoCmd(hexoDir)
		if r == 0:
			go()
	else:
		print("Please restart me and tell me what can i do for you?")
		exit()

def gitCmd(course_dir): # call git commands
	print("git add starting...")
	gitAdd = subprocess.run(["git","add","."],cwd=course_dir,universal_newlines=True,stdout=subprocess.PIPE)
	if gitAdd.returncode == 0:
		print(gitAdd.stdout)
		print("git add. done... And git commit starting...")
		comment_text = input("Please input comment message for this updating: ")

		gitCommit = subprocess.run(["git","commit","-m",comment_text],cwd=course_dir,universal_newlines=True,stdout=subprocess.PIPE)
		if gitCommit.returncode == 0:
			print(gitCommit.stdout)
			print("git commit done... And git push starting...")

			gitPush = subprocess.run(["git","push","-u",'origin','master'],cwd=course_dir,universal_newlines=True,stdout=subprocess.PIPE)
			if gitPush.returncode == 0:
				print(gitPush.stdout)
				print("git push done...")
				return 0
			else:
				print("returncode is %s git push exit..." % str(gitPush.returncode))
				return gitPush.returncode
		else:
			print("returncode is %s git commit. exit...Maybe no modify data" % str(gitCommit.returncode))
			return gitCommit.returncode
	else:
		print("returncode is %s git add. exit..." % str(gitAdd.returncode))
		return gitAdd.returncode

def note2temp(note_path,frontMatter): # copy the note file to the temp file
	# read the note and project
	try:
		print("Opening %s file with 'rt' mode..." % note_path)
		note_file = open(note_path,'rt') # open for reading with text mode

		print("Reading %s ...." % note_path)
		note_text = note_file.read()
	except IOError:
		print("IOError exception...")
		print("Maybe no such a file")
		return False
	else:
		print("Closing %s ...." % note_path)
		note_file.close()

	# create a temp file
	tfp = tempfile.TemporaryFile(mode='w+t') # default mode is w+b.

	# add a title  at the begining of the temp file
	print("Writing Front-Matter...")
	tfp.write(frontMatter)

	# copy the content of note and project into the temp file
	print("Writing note text...")
	tfp.write(note_text)

	tfp.seek(0)
	return tfp

def explore2temp(project_path,expFrontMatter): # copy the explore file to the temp file
	try:
		print("Opening %s file with 'rt' mode..." % project_path)
		project_file = open(project_path,'rt')

		print("Reading %s ...." % project_path)
		project_text = project_file.read()
	except IOError:
		print("IOError exception...")
		print("Maybe no such a file")
		return False
	else:
		print("Closing %s ...." % project_path)
		project_file.close()

	# create a temp file
	tfp = tempfile.TemporaryFile(mode='w+t') # default mode is w+b.

	# add a title  at the begining of the temp file
	print("Writing Front-Matter...")
	tfp.write(expFrontMatter)

	print("Writing project text...")
	tfp.write(project_text)
	tfp.seek(0)
	return tfp

def temp2hexo(tfp,hexoPath): # copy the temp file to the hexo file
	try:
		print("Opening %s file with 'w+t' mode..." % hexoPath)
		hfp = open(hexoPath,'w+')
		print("shutil.copyfileobj(tfp, hfp) start...")
	except IOError:
		print("IOError exception...")
		print("Maybe no such a file")
		return -1
	else:
		shutil.copyfileobj(tfp, hfp)
		print("shutil.copyfileobj(tfp, hfp) end...")
		print("Closing %s ...." % hexoPath)
		hfp.close()
		return 0

def hexoCmd(hexoDir): # call hexo commands
	print("sudo hexo generate starting....")
	p = subprocess.run(["sudo","hexo","generate"],cwd=hexoDir,universal_newlines=True,stdout=subprocess.PIPE)
	if p.returncode == 0:
		print("Hexo generate end....And hexo deploy starting....")
		r = subprocess.run(["sudo","hexo","deploy"],cwd=hexoDir,universal_newlines=True,stdout=subprocess.PIPE)
		if r.returncode == 0:
			print(r.stdout)
			print("Hexo deploy end....")
			print("Alright, all done.")
			return 0
		else:
			print("hexo deploy failed...")
			return -1			
	else:
		print("hexo generate failed...")
		return -1


if __name__ == '__main__':
	reExpression = r'^[0-9]$'
	chap = welcome()
	notePath = "/home/damao/project/Py103/Chap" + str(chap) +"/note/README.md" #
	projectPath = "/home/damao/project/Py103/Chap" + str(chap) +"/project/explore.md" #
	gitDir = "/home/damao/project/Py103" #
	hexoDir = "/home/damao/Public/simpleowen.github.io" #
	hexoExpPath = "/home/damao/Public/simpleowen.github.io/source/_posts/chap" + str(chap) + "explore.md"
	hexoNotePath = "/home/damao/Public/simpleowen.github.io/source/_posts/chap" + str(chap) + "note.md"
	# hexoPath = "/home/damao/Public/simpleowen.github.io/source/_posts/chaptest.md" # test

	weekJobs = [
	"Py103-ch0：预备周，熟悉学习节奏、配置基础环境",
	"Py103-ch1：CLI，开发一个运行在CLI环境的简易程序",
	"Py103-ch2：GUI，开发一个简易桌面版程序",
	"Py103-ch3：API，开发一个运行在CLI环境，可以获取实时数据的程序",
	"Py103-ch4：Web0，开发一个运行在web界面，部署在本地的程序",
	"Py103-ch5：Web1，开发一个运行在web界面，部署在本地，数据存储在数据库的程序",
	"Py103-ch6：PaaS，开发一个部署在Heroku平台，公网可访问的程序",
	"Py103-ch7：WeChat，开发一个基于微信的简易程序",
	"Py103-ch8：结业大作业，组队开发一个程序，方向自定",
	"Py103-ch9：结业路演，结业典礼"]

	frontMatter = """---
title: %s
tags: Py103
comments: true
date:
updated:
---
""" % weekJobs[chap]

	expFrontMatter = """---
title: %s explore
tags: Py103
comments: true
date:
updated:
---
"""  % weekJobs[chap][0:10]

	go()



```


---


### version 1.1

重新整理了需求和代码。

这个需求分为4块

- 执行3个git命令，git add, git commit, git push
- 复制文件，笔记内容复制到临时文件中
- 复制文件，给临时文件添加front-matter后，将其内容复制到博客文件中
- 执行2个hexo命令，hexo g, hexo d

![划分模块](http://7xrtxq.com1.z0.glb.clouddn.com/splitmodule.jpg)


这个版本将这几个功能封装成函数，提供交互来进行模块化操作

```
import subprocess
import tempfile
import shutil

# print welcome information
def welcome():
	welcomeWords = """
 		+---+---+---+---+---+---+---+
 		| W | E | L | C | O | M | E |
 		+---+---+---+---+---+---+---+
	"""
	print(welcomeWords)
	chap = int(input("Which chapter do you want to update? (0,1,2,3...9) "))
	return chap

# do what
def doSomething():
	doWhat = [
	"1.Git to Py103",
	"2.Note to Temp to Hexo",
	"3.Hexo to Blog"
	]

	for do in doWhat:
		print(do)
	what = int(input("What can i do for you? (1,2,3) "))
	if what == 1:
		return 1
	elif what == 2:
		return 2
	elif what == 3:
		return 3
	else:
		return -1

def go():
	iDo = doSomething()
	if iDo == 1:
		r = gitCmd(gitDir)
		go()
	elif iDo == 2:
		#tfp = note2temp(notePath,projectPath,frontMatter)
		tfp = note2temp(notePath,projectPath,"test for py") #test
		r = temp2hexo(tfp,hexoPath)
		if r == 0:
			go()
	elif iDo == 3:
		r = hexoCmd(hexoDir)
		if r == 0:
			go()
	else:
		print("Please restart me and tell me what can i do for you?")
		exit()

# call git commands
def gitCmd(course_dir):
	print("git add starting...")
	gitAdd = subprocess.run(["git","add","."],cwd=course_dir,universal_newlines=True,stdout=subprocess.PIPE)
	if gitAdd.returncode == 0:
		print(gitAdd.stdout)
		print("git add. done... And git commit starting...")
		comment_text = input("Please input comment message for this updating: ")

		gitCommit = subprocess.run(["git","commit","-m",comment_text],cwd=course_dir,universal_newlines=True,stdout=subprocess.PIPE)
		if gitCommit.returncode == 0:
			print(gitCommit.stdout)
			print("git commit done... And git push starting...")

			gitPush = subprocess.run(["git","push","-u",'origin','master'],cwd=course_dir,universal_newlines=True,stdout=subprocess.PIPE)
			if gitPush.returncode == 0:
				print(gitPush.stdout)
				print("git push done...")
				return 0
			else:
				print("returncode is %s git push exit..." % str(gitPush.returncode))
				return gitPush.returncode
		else:
			print("returncode is %s git commit. exit...Maybe no modify data" % str(gitCommit.returncode))
			return gitCommit.returncode
	else:
		print("returncode is %s git add. exit..." % str(gitAdd.returncode))
		return gitAdd.returncode

# copy the note file to the temp file
def note2temp(note_path,project_path,frontMatter):
	# read the note and project
	print("Opening %s file with 'rt' mode..." % note_path)
	note_file = open(note_path,'rt') # open for reading with text mode
	print("Opening %s file with 'rt' mode..." % project_path)
	project_file = open(project_path,'rt')

	print("Reading %s ...." % note_path)
	note_text = note_file.read()
	print("Reading %s ...." % project_path)
	project_text = project_file.read()

	print("Closing %s ...." % note_path)
	note_file.close()
	print("Closing %s ...." % project_path)
	project_file.close()

	# create a temp file
	tfp = tempfile.TemporaryFile(mode='w+t') # default mode is w+b.

	# add a title  at the begining of the temp file
	print("Writing Front-Matter...")
	tfp.write(frontMatter)

	# copy the content of note and project into the temp file
	print("Writing note text...")
	tfp.write(note_text)
	print("Writing project text...")
	tfp.write(project_text)
	tfp.seek(0)
	return tfp

# copy the temp file to the hexo file
def temp2hexo(tfp,hexoPath):
	print("Opening %s file with 'w+t' mode..." % hexoPath)
	hfp = open(hexoPath,'w+')
	print("shutil.copyfileobj(tfp, hfp) start...")
	shutil.copyfileobj(tfp, hfp)
	print("shutil.copyfileobj(tfp, hfp) end...")
	print("Closing %s ...." % hexoPath)
	hfp.close()
	return 0

# call hexo commands
def hexoCmd(hexoDir):
	print("sudo hexo generate starting....")
	p = subprocess.run(["sudo","hexo","generate"],cwd=hexoDir,universal_newlines=True,stdout=subprocess.PIPE)
	if p.returncode == 0:
		print("Hexo generate end....And hexo deploy starting....")
		r = subprocess.run(["sudo","hexo","deploy"],cwd=hexoDir,universal_newlines=True,stdout=subprocess.PIPE)
		if r.returncode == 0:
			print(r.stdout)
			print("Hexo deploy end....")
			print("Alright, all done.")

if __name__ == '__main__':
	chap = welcome()
	notePath = "/home/damao/project/testforpy103/Chap" + str(chap) +"/note/README.md" # a repo for testing
	projectPath = "/home/damao/project/testforpy103/Chap" + str(chap) +"/project/README.md" # a repo for testing
	gitDir = "/home/damao/project/testforpy103" # a repo for testing
	hexoDir = "/home/damao/Public/simpleowen.github.io" #
	# hexoPath = "/home/damao/Public/simpleowen.github.io/source/_posts/chap" + str(chap) + ".md"
	hexoPath = "/home/damao/Public/simpleowen.github.io/source/_posts/chaptest.md" # test

	weekJobs = [
	"Py103-ch0：预备周，熟悉学习节奏、配置基础环境",
	"Py103-ch1：CLI，开发一个运行在CLI环境的简易程序",
	"Py103-ch2：GUI，开发一个简易桌面版程序",
	"Py103-ch3：API，开发一个运行在CLI环境，可以获取实时数据的程序",
	"Py103-ch4：Web0，开发一个运行在web界面，部署在本地的程序",
	"Py103-ch5：Web1，开发一个运行在web界面，部署在本地，数据存储在数据库的程序",
	"Py103-ch6：PaaS，开发一个部署在Heroku平台，公网可访问的程序",
	"Py103-ch7：WeChat，开发一个基于微信的简易程序",
	"Py103-ch8：结业大作业，组队开发一个程序，方向自定",
	"Py103-ch9：结业路演，结业典礼"]

	frontMatter = """---
	title: %s
	tags: Py103
	comments: true
	date:
	updated:
	---
	""" % weekJobs[chap]
	go()

```

执行代码后，可以与用户交互了，输入相应的动作序号，可以执行相应的动作。

![交互界面](http://7xrtxq.com1.z0.glb.clouddn.com/inter.png)


还有3个问题待解决：

- 但还没有异常处理机制，当文件不存在时会不正常退出

- 在需要输入数字的地方，如果输入其他字符也会异常

- 增加正常退出机制，如输入某个组合键退出程序

----

### version 1.0

读取文件首先得知道文件在哪里。

课程仓库目录和文件比较有规律，
```
.
├── Chap0
│   ├── note
│   │   └── README.md
│   └── project
│       └── README.md
├── Chap1
│   ├── note
│   │   └── README.md
│   └── project
│       └── README.md
├── Chap2
│   ├── note
│   │   └── README.md
│   └── project
│       └── README.md
├── Chap3
│   ├── note
│   │   └── README.md
│   └── project
│       └── README.md
```

博客仓库中的目录`/home/damao/Public/simpleowen.github.io/source/_posts/`用来存放新文章

文件能找到了，需要读取文件内容。

可以用open函数来打开文件，read函数进行内容读取

内容读取后，需将其复制到临时文件中。

这时想到之前看过的2期优秀学员笔记中有使用tempfile来生成临时文件，于是去查[官方文档](https://docs.python.org/3/library/tempfile.html?highlight=tempfile#module-tempfile)，可以用函数tempfile.TemporaryFile(mode='w+b', buffering=None, encoding=None, newline=None, suffix=None, prefix=None, dir=None)来实现。

临时文件生成后，需要在开头写入博客标题，很自然想到seek()函数将文件指针移到0进行操作，接着写入从课程仓库中读取的笔记内容

临时文件还需要复制到博客仓库中，这时想到之前看过的一篇文章，印象中python有复制文件的模块，再进行搜索，找到了shutil模块

到这里，博客文章有了，只需要执行hexo命令了。

2期优秀学员的笔记再次帮我找到了[subprocess](https://docs.python.org/3/library/subprocess.html?highlight=subprocess#module-subprocess)模块。

感觉这个subprocess比较好玩、简单，而且文件提取、复制肯定是可以的，所以解决调用命令的问题，整个问题解决就有希望了，那就从subprocess开始吧。

看到这个函数加上简单的参数文档，就直接在编辑器里边开始试验了

subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, timeout=None, check=False, encoding=None, errors=None)

后面参数都可以省略，那就先省略吧。

在Sublime Text中写下
```
import subprocess

subprocess.run("sudo hexo g","/home/damao/Public/simpleowen.github.io")

```
执行，发生异常
```
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    subprocess.run("sudo hexo g","/home/damao/Public/simpleowen.github.io")
  File "/home/damao/anaconda3/lib/python3.5/subprocess.py", line 693, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/home/damao/anaconda3/lib/python3.5/subprocess.py", line 855, in __init__
    raise TypeError("bufsize must be an integer")
TypeError: bufsize must be an integer
```
bufsize必须为整型？在这个函数里边哪里有bufsize参数？于是回到文档硬着头皮接着看，发现run跟Popen函数有点关系，Popen参数里边就有这个bufsize。

可是这个bufsize放到run的哪个位置呢，当时并没有想到命名参数，这说明对python的特性还是不熟啊。

于是调整了许多次run函数，
```
subprocess.run(["hexo","generate","/home/damao/Public/simpleowen.github.io"],stdout=subprocess.PIPE)    

subprocess.run(["sudo hexo generate","/home/damao/Public/simpleowen.github.io"],universal_newlines=True,stdout=subprocess.PIPE,shell=True)  

subprocess.run("sudo hexo generate",cwd="/home/damao/Public/simpleowen.github.io",universal_newlines=True,stdout=subprocess.PIPE,shell=True)  

subprocess.run(["sudo","hexo","generate"],cwd="/home/damao/Public/simpleowen.github.io",universal_newlines=True,stdout=subprocess.PIPE)    

```
一边调整，一边试验，一边查资料，

几经折腾，总算搞明白了run函数几个要点

- 命令参数如果是字符串形式，shell要等于True，如果是列表形式则不需要

- 让命令在特定目录下执行，使用命名参数cwd等于该目录

- 如果要获得通用文本输出信息，则让universal_newlines=True

- 要获得命令执行后的输出，加上stdout=subprocess.PIPE，执行后,print(stdout)

Hexo命令成功在python中调用，所以调用git命令也可以使用相同的方案。

接着开始整文件提取并生成临时文件。

提取文件内容简单，open呐
```
note_path = ""/home/damao/project/Py103/Chap0/note/README.md""

f = open(note_path,'r')
```

生成临时文件也简单，tempfile文档里面很清楚了
```
tf = tempfile.TemporaryFile()

```

然后读取笔记内容，写入临时文件

```
note_text = f.read()
tf.write(note_text)
```

麻烦事在这出现了

执行后，异常

```
Traceback (most recent call last):
  File "test1.py", line 10, in <module>
    tf.write(note_text)
TypeError: a bytes-like object is required, not 'str'
```
临时文件对象要求写入类字节对象，而note_text是字符串对象。

那note_text怎么转换成字节对象呢？

在tempfile文档的[例子](https://docs.python.org/3/library/tempfile.html?highlight=tempfile#examples)中看到，字符串以字节对象进行写入

```
>>> import tempfile

# create a temporary file and write some data to it
>>> fp = tempfile.TemporaryFile()
>>> fp.write(b'Hello world!')

```
那怎样将note_text转为b呢？

bnote_text?

b(note_text)?

都不对。

note_text是从note笔记中读取的内容，open函数有一个b模式

修改open函数

```
import tempfile
note_path = "/home/damao/project/Py103/Chap0/note/README.md"
f = open(note_path,'rb') # add 'b' mode
note_text = f.read()
fp = tempfile.TemporaryFile()
fp.write(note_text)
print(fp.read())
```
执行正常。

到这里，只剩下一个主要任务：将临时文件复制到博客仓库文章发布目录下

复制文件使用[shutil模块](https://docs.python.org/3/library/shutil.html?highlight=shutil#module-shutil)

查看文档，发现有多种文件复制方式

> shutil.copyfileobj(fsrc, fdst[, length])

> shutil.copyfile(src, dst, *, follow_symlinks=True)

> shutil.copy(src, dst, *, follow_symlinks=True)

> shutil.copy2(src, dst, *, follow_symlinks=True)


由于不知道上面生成的临时文件路径，而且临时文件指针只要不关闭，在下面的代码中还是可以使用的，所以就选择第一种方式copyfileobj来进行文件复制

```
import tempfile
import shutil

note_path = "/home/damao/project/Py103/Chap0/note/README.md"
f = open(note_path,'rb')
note_text = f.read()

fp = tempfile.TemporaryFile()
fp.write(note_text)

hexo_file = "/home/damao/Public/simpleowen.github.io/source/_posts/test.md"
hfp = open(hexo_file,'w+')

shutil.copyfileobj(fp, hfp)


```
执行正常，在博客目录中也有test.md文件，但是没有内容。

思来想去，应该是文件指针的问题。临时文件指针在执行write函数后，就走到文件末尾了，而根据shutil文档的描述，

> Note that if the current file position of the fsrc object is not 0, only the contents from the current file position to the end of the file will be copied.

copyfileobj只复制文件指针当前位置开始到文件结束位置的内容

所以，在复制动作之前，将临时文件指针拨到文件开头位置seek(0)

```
import tempfile
import shutil

note_path = "/home/damao/project/Py103/Chap0/note/README.md"
f = open(note_path,'rb')
note_text = f.read()

fp = tempfile.TemporaryFile()
fp.write(note_text)

fp.seek(0)

hexo_file = "/home/damao/Public/simpleowen.github.io/source/_posts/test.md"
hfp = open(hexo_file,'w+')

shutil.copyfileobj(fp, hfp)

```

执行时却报出了另一个异常

```
Traceback (most recent call last):
  File "test.py", line 11, in <module>
    shutil.copyfileobj(fp, hfp)
  File "/home/damao/anaconda3/lib/python3.5/shutil.py", line 76, in copyfileobj
    fdst.write(buf)
TypeError: write() argument must be str, not bytes

```

其实将博客文章以'b'模式打开是可以解决这个异常的，前面临时文件写入是以'b'模式写入，而博客文章却以默认的't'模式打开，所以字符编码不一致导致copyfileobj调用时无法写入

> hfp = open(hexo_file,'w+b')

只是后来写这篇日记才发现这个问题。

当时想的是，复制文件需要str,而临时文件写入了byte,所以得推翻临时文件的模式，重新写入str到文件中。

于是回过头屡这个字符编码的问题，

在看open函数文档时，发现有一个't'模式(文本模式)是默认模式，

查阅tempfile文档，发现tempfile.TemporaryFile()函数的第一个模式参数默认值是'w+b'，可以把这个参数修改为'w+t'，

这样的话，笔记文件、临时文件、博客文件的字符编码就都统一了。

立即修改测试代码


```
import tempfile
import shutil
note_path = "/home/damao/project/Py103/Chap0/note/README.md"
f = open(note_path,'r') # 默认是't'模式
note_text = f.read()
fp = tempfile.TemporaryFile('w+t') # 手动修改临时文件为't'模式
fp.write(note_text)
fp.seek(0)
hexo_file = "/home/damao/Public/simpleowen.github.io/source/_posts/test.md"
hfp = open(hexo_file,'w+')  # 默认是't'模式
shutil.copyfileobj(fp, hfp)

```
执行成功，而且博客文章获得了笔记文章的内容。

出代码

至此，为实现开头提出的需求而要解决的主要问题都得到解决。

果断上代码

```
# coding:utf-8

import os
import subprocess
import tempfile
import shutil
from sys import argv

# git commands

git_dir = "/home/damao/project/Py103"
print("git add. start...")
gitadd_subprocess = subprocess.run(["git","add","."],cwd=git_dir,universal_newlines=True,stdout=subprocess.PIPE)
if gitadd_subprocess.returncode == 0:
	print(gitadd_subprocess.stdout)
	print("git add. done...")
	print("git commit start...")
	comment_text = input("Please input comment message for this commit:")
	gitcommit_subprocess = subprocess.run(["git","commit","-m",comment_text],cwd=git_dir,universal_newlines=True,stdout=subprocess.PIPE)
	if gitcommit_subprocess.returncode == 0:
		print(gitcommit_subprocess.stdout)
		print("git commit done...")
		print("git push start...")
		gitpush_subprocess = subprocess.run(["git","push","-u",'origin','master'],cwd=git_dir,universal_newlines=True,stdout=subprocess.PIPE)
		if gitpush_subprocess.returncode == 0:		
			print(gitpush_subprocess.stdout)
			print("git push done...")
		else:
			print("returncode is %s git push exit..." % str(gitpush_subprocess.returncode))			
	else:
		print("returncode is %s git commit. exit..." % str(gitcommit_subprocess.returncode))
else:
	print("returncode is %s git add. exit..." % str(gitadd_subprocess.returncode))


# locate the file

chap = argv[1]

title_list = [
"Py103-ch0：预备周，熟悉学习节奏、配置基础环境",
"Py103-ch1：CLI，开发一个运行在CLI环境的简易程序",
"Py103-ch2：GUI，开发一个简易桌面版程序",
"Py103-ch3：API，开发一个运行在CLI环境，可以获取实时数据的程序",
"Py103-ch4：Web0，开发一个运行在web界面，部署在本地的程序",
"Py103-ch5：Web1，开发一个运行在web界面，部署在本地，数据存储在数据库的程序",
"Py103-ch6：PaaS，开发一个部署在Heroku平台，公网可访问的程序",
"Py103-ch7：WeChat，开发一个基于微信的简易程序",
"Py103-ch8：结业大作业，组队开发一个程序，方向自定",
"Py103-ch9：结业路演，结业典礼"]

note_dir = "/home/damao/project/Py103/Chap" + chap +"/note/"
project_dir = "/home/damao/project/Py103/Chap" + chap +"/project/"

note_path = "/home/damao/project/Py103/Chap" + chap +"/note/README.md"
project_path = "/home/damao/project/Py103/Chap" + chap +"/project/README.md"

# read the note and project

note_file = open(note_path,'rt') # open for reading with text mode
project_file = open(project_path,'rt')

note_text = note_file.read()
project_text = project_file.read()

note_file.close()
project_file.close()

# create a temp file

tfp = tempfile.TemporaryFile(mode='w+t')

# add a title  at the begining of the temp file

title = """
---
title: %s
tags: Py103
comments: true
date:
updated:
---
""" % title_list[int(chap)]

tfp.write(title)

# copy the content of note and project into the temp file

tfp.write(note_text)
tfp.write(project_text)
tfp.seek(0)

# copy the temp file to the hexo

hexo_path = "/home/damao/Public/simpleowen.github.io/source/_posts/" + title_list[int(chap)] + ".md"
hfp = open(hexo_path,'w+')

shutil.copyfileobj(tfp, hfp)

hfp.close()

# call hexo g and hexo d

p = subprocess.run(["sudo","hexo","generate"],cwd="/home/damao/Public/simpleowen.github.io",universal_newlines=True,stdout=subprocess.PIPE)
if p.returncode == 0:
	r = subprocess.run(["sudo","hexo","deploy"],cwd="/home/damao/Public/simpleowen.github.io",universal_newlines=True,stdout=subprocess.PIPE)
	if r.returncode == 0:
		print(r.stdout)

# done
print("Alright, all done.")


```
