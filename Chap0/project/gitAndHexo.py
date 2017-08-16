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

