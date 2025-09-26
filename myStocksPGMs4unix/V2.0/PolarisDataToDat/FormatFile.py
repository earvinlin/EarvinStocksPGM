import sys
import os 
import time

insertCnt = 0 
isFirstLine = True
try:
	print("[FormatFile.py] 開始執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))

	if len(sys.argv) < 3 :
		print("You need input two parameter(fmt : inputFileName outputFileName)")
		print("syntax : C:\python FormatFile.py 2002-20170816.csv 2002.txt")
		sys.exit()

	loadFileDir = "csv\\"
	saveFileDir = "txt\\"
	inputFile = sys.argv[1]
	outputFile = sys.argv[2]
	
	outfile = open(saveFileDir + outputFile, 'w')

	with open(loadFileDir + inputFile, 'r') as infile :
		for eachLine in infile :
#			第1列為標題列，要另外處理
			if isFirstLine :
				eachLine.replace(" ", "")
#               各欄位間的空白全都要去掉
				omitSpace = eachLine.replace(" ", "")
#               「騰落指標」有2個，要把第2個換成「漲跌家數」
				position = omitSpace.rfind("騰落指標")
				outputString = omitSpace[0:position] + "漲跌家數" + omitSpace[position+4:len(omitSpace)]
				print("Write Data = " + outputString)
				outfile.write(outputString)
				isFirstLine = False
			else :
				outfile.write(eachLine)
			insertCnt += 1

	infile.close()
	outfile.close()
	
except IOError as err :
	print('File error : ' + str(err))

print("資料處理完成!! 共 " + str(insertCnt) + " 筆。")
print("[FormatFile.py] 結束執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))
