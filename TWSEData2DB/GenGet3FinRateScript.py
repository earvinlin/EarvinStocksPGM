"""
20220522 產生執行_GetDailyRatios.py的script
         需要輸入的參數：檔案路徑 
         -------------------------------------------------------------------------
         Content :
         -------------------------------------------------------------------------
         python3 GenGet3FinRateScript.py /Users/earvin/workspaces/GithubProjects/GoodinfoData2DB/Data/TXT/salemon/22020520/ 

https://www.twse.com.tw/zh/page/trading/exchange/BWIBBU_d.html
"""
import sys
import os 
import time
import platform

print("[GenGet3FinRateScript.py] 開始執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

outputFile = ""
processCnt = 0
errorCnt = 0
try:
	print("[GenGet3FinRateScript.py] 開始執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

	if len(sys.argv) < 3 :
		print("You need input two parameter : 起日 迄日")
		print("syntax(windows)    : C:\python GenInsertData2DbScripts.py Data\\3Rate\\")
		print("syntax(imac/linux) : $python3 GenInsertData2DbScripts.py Data/TXT/salemon/20220522/")
		sys.exit()

	beginDate = int(sys.argv[1])
	endDate = int(sys.argv[2])

	print ("beginDate= ", beginDate, ", endDate= ", endDate)

	# 設定檔案存取路徑
	pythonCompiler = ""
	if platform.system() == "Windows" :
		pythonCompiler = "python"
		outputFile = "_GenGet3FinRateScript.Bat"
	else :
		pythonCompiler = "python3"
		outputFile = "_GenGet3FinRateScript.sh"

	outfile = open(outputFile, 'w')

    # python GenGet3FinRateScript.py 20200101 20210131
	while beginDate <= endDate :
		print(beginDate)
#		Write out contents
#		python 01_getStocksDailyRatiosData.py 20211027
#		python 01_formatStocksDailyRatiosData.py 20211027

		writeContent1 = pythonCompiler + " 01_getStocksDailyRatiosData.py " + str(beginDate) + "\n"
#		print("Content: " + writeContent)
		outfile.write(writeContent1)
		writeContent2 = pythonCompiler + " 01_formatStocksDailyRatiosData.py " + str(beginDate) + "\n" 
#		print("Content: " + writeContent)
		outfile.write(writeContent2)
		processCnt += 1

		if str(beginDate)[4:6] == "01" or str(beginDate)[4:6] == "03" or \
			str(beginDate)[4:6] == "05" or str(beginDate)[4:6] == "07" or \
			str(beginDate)[4:6] == "08" or str(beginDate)[4:6] == "10" or \
			str(beginDate)[4:6] == "12" :
			
			if int(str(beginDate)[6:8]) < 31 :
				beginDate += 1
			else :
				if int(str(beginDate)[4:6]) < 12 :
					beginDate = beginDate + 100 - int(str(beginDate)[6:8]) + 1
				else :
					beginDate = beginDate - int(str(beginDate)[4:6]) - int(str(beginDate)[6:8]) + 101

	outfile.close()

	print("資料處理完成!! 共 " + str(processCnt) + " 筆。")
	print("[GenGet3FinRateScript.py] 結束執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

except IOError as err :
	print('File error : ' + str(err))
