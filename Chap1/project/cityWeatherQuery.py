import datetime
def getWeatherData(): # 获取天气数据
	# weatherDict = {}
	with open(weatherFilePath,'r') as wf:
		for f in wf:
			weatherDict[f.split(",")[0].strip()] = f.split(",")[1].strip()
	return weatherDict

def getHelp(): # 获取帮助信息
	# global helpInfo
	print(helpInfo)

def setHistory(city,weatherStatus): # 保存历史查询记录
	#加入序号，时间，城市名，天气状况
	# global historyList
	no = len(historyList)#获取列表长度
	queryTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	historyList.append(tuple((no + 1,queryTime,city,weatherStatus))) #转换成4元元组

def getHistory(): # 获取历史查询信息
	# global historyList
	if len(historyList) == 0: print("没有历史查询信息")
	for history in historyList:
		print(history[0],history[1],history[2],history[3]) # 访问元组

def getCityWeather(info,weatherData): # 查询天气信息
	print("%s 的天气状况是： %s" % (info,weatherData[info]))
	setHistory(info,weatherData[info])

def exitApp(): # 退出程序
	# exitCode = 0
	getHistory()
	exit(0)

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
	weatherFilePath = "weather_info.txt"
	helpInfo = """
	输入 城市名，查询该城市的天气；
	输入 h或help或帮助，获取帮助文档；
	输入 history或历史，获取查询历史；
	输入 q或quit或退出，退出天气查询系统。
	"""
	historyList = []
	weatherDict = getWeatherData()
	go(weatherDict)
