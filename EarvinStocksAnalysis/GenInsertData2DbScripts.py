"""
20220522 產生執行InsertData2DbByFile.py的script (Copy From Goodinfo Project)
         需要輸入的參數：檔案路徑 
         -------------------------------------------------------------------------
         Content :
         -------------------------------------------------------------------------
         [windows] -- 可使用相對路徑
	    	python GenInsertData2DbScripts.py DATA\\LEGAL\\SQL\\20190101-20191231\\ 

		 [imac / linux] 絕對路徑可正常執行 (??? untest)
         python3 GenInsertData2DbScripts.py /Users/earvin/workspaces/GithubProjects/EarvinStocksPGM/EarvinStocksAnalysis/ 

"""
import sys
import os 
import time
import platform

print("[GenInsertData2DbScripts.py] 開始執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

loadFileDir = ""
outputFile = ""
processCnt = 0
errorCnt = 0
try:
	print("[FormatFile.py] 開始執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

	if len(sys.argv) < 2 :
		print("You need input one parameter : 檔案目錄")
		print("syntax(windows)    : C:\python GenInsertData2DbScripts.py DATA\\LEGAL\\SQL\\20190101-20191231\\")
		print("syntax(imac/linux) : $python3 GenInsertData2DbScripts.py Data/LEGAL/SQL/20190101-20191231/")
		sys.exit()

	# 設定檔案存取路徑
	pythonCompiler = ""
	if platform.system() == "Windows" :
		pythonCompiler = "python"
		loadFileDir = sys.argv[1]
		outputFile = "_InsertStocksData2DB.Bat"
	else :
		pythonCompiler = "python3"
		loadFileDir = "/Users/earvin/workspaces/GithubProjects/EarvinStocksPGM/EarvinStocksAnalysis/" + sys.argv[1]
		outputFile = "_InsertStocksData2DB.sh"

	print("loadFile dir: " + loadFileDir)

	outfile = open(outputFile, 'w')

    # python InsertData2DbByFile.py DATA\\LEGAL\\SQL\\20190101-20191231\\ 1101.txt
	# 20220522 取得要處理的檔案資料
	files = os.listdir(loadFileDir)
	# 以迴圈處理
	for inputFile in files:
		relativePath = os.path.join(loadFileDir, inputFile)
		if os.path.isfile(relativePath) :
			print("檔案：", inputFile)

		stockCode = inputFile[:4]
		writeContent = pythonCompiler + " InsertData2DbByFile.py " + loadFileDir + " " + stockCode + ".txt"
#		print("Content: " + writeContent)
		outfile.write(writeContent + "\n")
		processCnt += 1

	outfile.close()

	print("資料處理完成!! 共 " + str(processCnt) + " 筆。")
	print("[GenInsertData2DbScripts.py] 結束執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

except IOError as err :
	print('File error : ' + str(err))
