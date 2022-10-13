"""
20221013 產生執行_InsertDailyRatio.py的批次script
		 (程式放在「…\OneDrive\myStocksPGMs\V2.0\PythonTools\【新增個股3項財務指標】」)
         需要輸入的參數：檔案路徑 
         ----------------------------------------------------------------------------
         Content :
         ----------------------------------------------------------------------------
         win : python GenInsert3FinRate2DBScript.py 起日(fmt: yyyymmdd) 迄日(fmt: yyyymmdd)
		 imac: python3 GenInsert3FinRate2DBScript.py 起日(fmt: yyyymmdd) 迄日(fmt: yyyymmdd)
"""
import sys
import os 
import time
import platform

outputFile = ""
processCnt = 0
errorCnt = 0
try:
	print("[GenInsert3FinRate2DBScript.py] 開始執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

	if len(sys.argv) < 3 :
		print("You need input two parameter : 起日 迄日")
		print("syntax(windows)    : C:\python GenInsert3FinRate2DBScript.py 20210101 20221012")
		print("syntax(imac/linux) : $python3 GenInsert3FinRate2DBScript.py 20210101 20221012")
		sys.exit()

	beginDate = int(sys.argv[1])
	endDate = int(sys.argv[2])

	print ("beginDate= ", beginDate, ", endDate= ", endDate)

	# 設定檔案存取路徑
	pythonCompiler = ""
	if platform.system() == "Windows" :
		pythonCompiler = "python"
		outputFile = "_GenInsert3FinRateDBScript.Bat"
	else :
		pythonCompiler = "python3"
		outputFile = "_GenInsert3FinRateDBScript.sh"

	outfile = open(outputFile, 'w', encoding="utf8")

	while beginDate <= endDate :
		chineseDate = beginDate - 19110000
		writeContent = pythonCompiler + " 02_insertDailyRatiosToMySQLDB.py " + \
            str(chineseDate) + " stocks_個股日本益比殖利率及股價淨值比-" + \
			str(beginDate) + ".txt\n"
		outfile.write(writeContent)
		processCnt += 1

		if str(beginDate)[4:6] == "01" or str(beginDate)[4:6] == "03" or \
			str(beginDate)[4:6] == "05" or str(beginDate)[4:6] == "07" or \
			str(beginDate)[4:6] == "08" or str(beginDate)[4:6] == "10" or \
			str(beginDate)[4:6] == "12" :
			if int(str(beginDate)[6:8]) < 31 :
				beginDate += 1
			else :
				if int(str(beginDate)[4:6]) < 12 :
					beginDate = beginDate - int(str(beginDate)[6:8]) + 101
				else :
					beginDate = beginDate - int(str(beginDate)[4:8]) + 10101
			continue

		if str(beginDate)[4:6] == "04" or str(beginDate)[4:6] == "06" or \
			str(beginDate)[4:6] == "09" or str(beginDate)[4:6] == "11" :	
			if int(str(beginDate)[6:8]) < 30 :
				beginDate += 1
			else :
				beginDate = beginDate - int(str(beginDate)[6:8]) + 101
			continue

		if str(beginDate)[4:6] == "02" :	
			day = 28
			WesternNewYear =  int(str(beginDate)[1:4])
			if not WesternNewYear%4 : 
				day = 28
			else :
				if not WesternNewYear%100 :	
					if not WesternNewYear%400 : 
						day = 29
					else :
						day = 28
				else :
					day = 29
			if int(str(beginDate)[6:8]) < day :
				beginDate += 1
			else :
				beginDate = beginDate - int(str(beginDate)[6:8]) + 101

	outfile.close()

	print("資料處理完成!! 共 " + str(processCnt) + " 筆。")
	print("[GenInsert3FinRate2DBScript.py] 結束執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

except IOError as err :
	print('File error : ' + str(err))
