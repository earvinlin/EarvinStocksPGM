import sys
import os 
import time

insertCnt = 0 
isFirstLine = True
try:
	print("[FormatFileGlobal.py] 開始執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))

	if len(sys.argv) < 3 :
		print("You need input two parameter(fmt : inputFileName outputFileName)")
		print("syntax : C:\python FormatFile.py stockno.csv stockno.txt")
		sys.exit()

	loadFileDir = "csv\\國際股票資料\\"
	saveFileDir = "txt\\"
	inputFile = sys.argv[1]
	outputFile = sys.argv[2]
	
	outfile = open(saveFileDir + outputFile, 'w')

	with open(loadFileDir + inputFile, 'r') as infile :
		for eachLine in infile :
#			日期分隔符號若為「-」，要改成「/」，
# 			要不程式InsertStocksFromPolarisToMySQLDB.py會異動失敗		
			eachLine = eachLine.replace("-", "/")
			omitSpace = eachLine.replace(" ", "")			
			position = omitSpace.find("\n")
#			第1列為標題列，要另外處理
			if isFirstLine :
#				日期,開盤,最高,最低,收盤,成交量,融資張數,融券張數, 騰落指標, 外資庫存, 投信庫存, 自營商庫存, 法人庫存, 未平倉量
				outputString = "日期,開盤,最高,最低,收盤,收盤(調),成交量,融資張數,融券張數,騰落指標,漲跌家數,外資庫存,投信庫存,自營商庫存,法人庫存,未平倉量\n"
				print("Write Data = " + outputString) 
				isFirstLine = False
			else :
				outputString = omitSpace[0:position] + ",0,0,0,0,0,0,0,0,0\n"

			outfile.write(outputString)
			insertCnt += 1

	infile.close()
	outfile.close()
	
except IOError as err :
	print('File error : ' + str(err))

print("資料處理完成!! 共 " + str(insertCnt) + " 筆。")
print("[FormatFileGlobal.py] 結束執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))
