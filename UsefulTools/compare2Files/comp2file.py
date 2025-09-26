import sys
import os 
import time
import platform

print("[GenInsertData2DbScripts.py] 開始執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

outputFile = "diff.txt"
processCnt = 0
errorCnt = 0
try:
    print("[FormatFile.py] 開始執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

    if len(sys.argv) < 3 :
        print("You need input two parameter : 檔案目錄")
        print("syntax(windows)    : C:\\python comp.py file1.txt file2.txt")
        print("syntax(imac/linux) : $python3 comp.py file1.txt file.txt")
        sys.exit()

    inputFile1 = sys.argv[1]
    inputFile2 = sys.argv[2]

    outfile = open(outputFile, 'w')
    file1 = open(inputFile1, 'r', encoding='utf-8')
    file2 = open(inputFile2, 'r', encoding='utf-8')
    lst1 = []
    lst2 = []

    for line in file1 :
        lst1.append(line.strip())
#    print(lst1)

    for line in file2 :
        lst2.append(line.strip())
#    print(lst2)

    count1 = 0
    count2 = 0
    c1 = lst1[count1]
    c2 = lst2[count2]

    flag = True
    print("flag= ", flag, "[len(lst1)]= ",len(lst1), "[len(lst2)]= ",len(lst2))

    while flag :
        if c1 == c2 :
            count1 = count1 + 1
            count2 = count2 + 1
        elif c1 < c2 :
            outfile.write(lst1[count1]+"\n")
            count1 = count1 + 1
        else :
            outfile.write(lst2[count2]+"\n")
            count2 = count2 + 1

        print("flag= ", flag, "count1= ", count1, ", count2= ", count2, "[len(lst1)]= ",len(lst1), "[len(lst2)]= ",len(lst2))
        if count1 >= (len(lst1)) or count2 >= (len(lst2)) :
            if count1 >= (len(lst1)) :
                while count2 < (len(lst2)-1) :
                    outfile.write(lst2[count2]+"\n")
                    count2 = count2 + 1
            if count2 >= (len(lst2)) :
                while count1 < (len(lst1)-1) :
                    outfile.write(lst1[count1]+"\n")
                    count1 = count1 + 1
            flag = False
        print("flag=", flag)

        if flag :
            print("flagaa=", flag)
            c1 = lst1[count1]
            c2 = lst2[count2]

    outfile.write("test"+"\n")
    processCnt += 1

    outfile.close()
    file1.close()
#    file2.close()


    print("資料處理完成!! 共 " + str(processCnt) + " 筆。")
    print("[GenInsertData2DbScripts.py] 結束執行時間：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

except IOError as err :
    print('File error : ' + str(err))


