## 本周任务笔记

探索python2和python3的差异

根据开智模因：信息的源头，自然想到要到[python官网](https://www.python.org/)去发现py2和py3的差异。
<!-- more -->
跟踪python版本的发布，关注版本变更日志是一个不错的办法。可以到[What is New](https://docs.python.org/3/whatsnew/index.html)查看历史更新。

如果从头开始看，工作量有点大，还好前辈们早已整理了各种资料供总体概览，比如[这里](http://python-future.org/compatible_idioms.html)和[这里](http://nbviewer.jupyter.org/github/rasbt/python_reference/blob/master/tutorials/key_differences_between_python_2_and_3.ipynb?create=1)，还有[这里](http://www.runoob.com/python/python-2x-3x.html)就用代码的形式展现了py2和py3的差异。

目前阶段可能会遇到的差异

| items | Python2         | Python3     |
| ----- | ---------   | -------- |
| 打印 | print 'Hello,World' <br>print('Hello,World')  |print('Hello,World')|
| 等待用户输入 | [input()](https://docs.python.org/2/library/functions.html?highlight=input#input)<br>[raw_input()](https://docs.python.org/2/library/functions.html?highlight=raw_input#raw_input)   | [input()](https://docs.python.org/3/library/functions.html?highlight=input#input) |
| 整型 | long<br>int | int |
| 整数除法 | 3 / 2 = 1  | 3 / 2 = 1.5  |

python3源码默认使用utf-8进行编码，使得在注释中使用中文再也不用在代码第一句使用`# coding:utf-8`了，

```
print('人生苦短，Python当歌') # 打印一个句子

damao@damao:~/project/automate$ python test.py
人生苦短，Python当歌

```

并且使用中文进行变量命名也是合法的，如：我 = ‘me’

```
damao@damao:~$ python
Python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  2 2016, 17:53:06)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 我 = 'me'
>>> print(我)
me
>>>
```

python3新增了两个字节类[bytes](https://docs.python.org/3/library/functions.html?highlight=bytes#bytes) and [bytearray](https://docs.python.org/3/library/functions.html?highlight=bytes#bytearray)


字典类的keys()、values()、items()方法在py2中返回一个list，py3返回[迭代器](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143178254193589df9c612d2449618ea460e7a672a366000)



## 遇到一个问题

**自主探索的最佳姿势，不是沿知识树学习，而是解决问题。**

在本周的任务中，碰到一个问题：我选择将笔记发布在个人博客网站上，这样的话在课程仓库中写好笔记后，还需要复制一份到[hexo](https://hexo.io/zh-cn/)博客仓库中，再分别执行命令来进行github提交，所以就想着用python代码来自动化实现这个过程。


问题过程分析

在执行git命令时同时执行hexo命令，所以得让python脚本执行hexo命令

本地分别有一个课程仓库目录和博客仓库目录，所以在课程仓库中写好笔记后，需要将笔记文件拷贝到博客仓库的目录下

因为Hexo有其特有的[标题格式](https://hexo.io/zh-cn/docs/front-matter.html)，所以不能直接拷贝笔记文件到博客仓库目录下，需要先将笔记文件内容取出生成一个临时文件，在临时文件的开头增加标题格式部分，再将临时文件写入到博客仓库目录下

最后再执行hexo g 和hexo d命令来实现博客上传更新

更加详细的过程分析

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


## 总结：

#### 使用的模块

- subprocess：生成新的进程

- tempfile：生成临时文件或目录

- shutil：复制文件或目录



#### 遇见的概念

- [Python Enhancement Proposal(PEP)  python增强建议书](https://www.python.org/dev/peps/)

- 理解容器、可迭代对象、迭代器、生成器
[参考](http://nvie.com/posts/iterators-vs-generators/)

- 理解迭代、循环、遍历、递归

循环(loop)：重复的动作都可以称为循环，所以递归、遍历、迭代也是一种循环
递归(recursion)：函数调用自己
遍历(traversal)：访问非线性数据结构的每一项
迭代(iterate)：访问线性数据结构的每一项


## 疑问

1. 如何提高英文文档阅读理解能力？

1. 如何写笔记更有效果？

I.等整个思路理顺，形成了代码后才写?
这种写法有两个情况，一是写探索过程，二是省略探索的过程，直接写出逻辑清晰的过程分析和代码
如果第一种情况完整写下探索的过程，这种情况可能有些细节会忘记，也可能有些细节会受到已经解决思路的影响，有种放弃逻辑回到混乱的感觉，写得有点痛苦，而且随着一步步挖掘，涉及的东西越来越多，有种长篇大论没有明确主题的感脚；第二种情况就简洁明了，看着会比较舒服

II.在探索思考的过程就开始一边写?  
如果是在探索过程中就开始写的话，写出来会比较混乱，而且耗时，可能还会打断探索过程
