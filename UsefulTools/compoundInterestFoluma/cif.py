"""
Foluma :
    A = P(1 + r/n)^(nt)
Param :
    Here's what each symbol means:
    A = final amount (including interest)
    P = principal amount (initial investment)
    r = annual interest rate (in decimal)
    n = number of times interest is compounded per year
    t = number of years
Example :
    pyh=thon3 cif.py type p1 p2 p3 p4
    if type == A , 求 A ; p1=P, p2=r, p3=n, p4=t
    if type == P , 求 P ; p1=A, p2=r, p3=n, p4=t
    if type == r , 求 r ; p1=A, p2=P, p3=n, p4=t
    if type == n , 求 n ; p1=A, p2=P, p3=r, p4=t
    if type == t , 求 t ; p1=A, p2=P, p3=r, p4=n
"""
import sys
import os 
import time
import platform
import math

# 無法直接代數解出這個公式無法直接代數解出 𝑛，因為 𝑛同時出現在分母與指數中。
# 所以我們需要使用數值方法（例如牛頓法或二分搜尋）來近似求解。
def calculate_periods(P, A, r, t, precision=1e-6, max_iter=10000):
    if P <= 0 or A <= 0 or r <= 0 or t <= 0:
        raise ValueError("所有參數必須為正數")

    # 搜尋範圍：每年複利次數 n 通常在 1 到 365 之間
    low = 0.0001
    high = 1000
    iter_count = 0

    while iter_count < max_iter:
        n = (low + high) / 2
        estimated_A = P * (1 + r / n) ** (n * t)

        if abs(estimated_A - A) < precision:
            return n
        elif estimated_A < A:
            low = n
        else:
            high = n

        iter_count += 1

    raise RuntimeError("無法在指定精度內找到解")




type = sys.argv[1]
theA = 0
theP = 0
theR = 0
theN = 0
theT = 0

print("type= ", type)

# Case 求 A (最終金額)
if type == "A" :
#   A = P(1 + r/n)^(nt)
    print("In Type A")
    theP = float(sys.argv[2])
    theR = float(sys.argv[3])
    theN = float(sys.argv[4])
    theT = float(sys.argv[5])
    
    theA = theP * (1 + theR / theN) ** (theN * theT)
    print(f"theA= {theA:.2f}")

# Case 求 P (初始金額)
elif type == "P" :
#   A = P(1 + r/n)^(nt)
    print("In Type P")
    theA = float(sys.argv[2])
    theR = float(sys.argv[3])
    theN = float(sys.argv[4])
    theT = float(sys.argv[5])
    
    theP = theA / (1 + theR / theN) ** (theN * theT)
    print(f"theP= {theP:.2f}")

# Case 求 r
elif type == "r" :
#   r = n * ((A / P) ** (1 / (n * t)) - 1)
    theA = float(sys.argv[2])
    theP = float(sys.argv[3])
    theN = float(sys.argv[4])
    theT = float(sys.argv[5])

    theR = theN * ((theA / theP) ** (1 / (theN * theT)) - 1)
    print(f"theR= {theR:.2f}")

# Case 求 n (期數) ; 20240714 有問題，要再確認為何？
elif type == "n" :
    theA = float(sys.argv[2])
    theP = float(sys.argv[3])
    theR = float(sys.argv[4])
    theT = float(sys.argv[5])

    theP = 19
    theA = 30
    theR = 0.08
    theT = 5

    theN = calculate_periods(theP, theA, theR, theT)
    print(f"theN= {theN:.2f}")

# Case 求 t
elif type == "t" :
    theA = float(sys.argv[2])
    theP = float(sys.argv[3])
    theR = float(sys.argv[4])
    theN = float(sys.argv[5])

    theT = math.log(theA / theP) /  (theN * math.log(1 + theR / theN))
    print(f"theT= {theT:.2f}")

else :
    print("No meet type!!!")


