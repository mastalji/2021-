from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import xlsxwriter
import random

yf.pdr_override()

samsung = pdr.get_data_yahoo('BTC-USD', start='2020-10-26', end='2021-10-26')
print(samsung)
print('.')
print(samsung.index)#날짜 꽁으로 뽑기 가능
print('.')
print(samsung.columns) 
print('.')

div = 1
lastdiv = 1
maxmoney = 100000000
returnindex = 1
def sumdev(k): #돈 넣는 비율 계산
    return k*div

#이동평균선
samsungopen = list(samsung.Open)
samsungclose = list(samsung.Close)

moveavg5 = []
for i in range(4):
    moveavg5.append(0)
for i in range(4,len(samsungopen)):
    avg5 = 0
    a = 0
    for k in range(0,5):
        a += samsungopen[i-k]
    avg5 = a/5
    moveavg5.append(avg5)
print(moveavg5)

moveavg20 = []
for i in range(19):
    moveavg20.append(0)
for i in range(19,len(samsungopen)):
    avg20 = 0
    a = 0
    for k in range(0,20):
        a += samsungopen[i-k]
    avg20 = a/20
    moveavg20.append(avg20)
print(moveavg20)

#유전 알고리즘 테스트 반복
def visual(x):
        return x*10
    
while True:
    #for 이어짐
    #돈
    money=100000000 #1억
    samsungstock=0
    
#5,20이동평균선 알고리즘 테스트
    samsungindex = list(samsung.index)
    buyindex = {}
    for i in samsungindex:
        buyindex[i] = 0
    
    sellindex = {}
    for i in samsungindex:
        sellindex[i] = 0.5

#1. 매수조건 (첫날에는 구매하지 않음)
    for i in range(21,len(samsungopen)):
        if int(samsungopen[i]) == 0:
            continue
        if samsungopen[i] > samsungopen[i-1] and samsungopen[i] > moveavg5[i] and moveavg5[i] > moveavg20[i] and samsungclose[i-1] < samsungopen[i] and money > samsungopen[i]:
            buyindex[samsungindex[i]] = 1
            buying = int(sumdev(int(money/int(samsungopen[i]))))
            samsungstock += buying
            money -= buying*int(samsungopen[i])
#2. 매도조건
        if moveavg5[i] <= moveavg20[i] and samsungstock > 0:
            sellindex[samsungindex[i]] = 2
            selling = int((samsungstock))
            money += selling*int(samsungopen[i])
            samsungstock -= selling

#3. 결과 출력
    money += samsungstock*int(samsungopen[-1])
    print(money)
    print(money/100000000)
    print(div)
    print(".")
    maxmoney = max(money,maxmoney)

#4. 유전 알고리즘 반복 break
#    if money/100000000 >= 1.1: 
#        print(returnindex)
#        break
    if returnindex == 1000:
        print(returnindex)
        print(maxmoney)
        print(lastdiv)
        print(maxmoney/100000000)
        break
        
#5. break 실패시 다른 div 정하기
    returnindex += 1
    if maxmoney == money:
        lastdiv = div
        up = lastdiv*1.2
        down = lastdiv*0.8
        if up > 1:
            up = 1
        div = random.uniform(down,up)
    else:
        div = lastdiv
        up = lastdiv*1.2
        down = lastdiv*0.8
        if up > 1:
            up = 1
        div = random.uniform(down,up)
        
#exel
workbook = xlsxwriter.Workbook('samsung.xlsx')
worksheet = workbook.add_worksheet()

cell_format = workbook.add_format({'border': 1})
worksheet.set_column('A:A', 10)
worksheet.set_column('B:B', 10)
worksheet.set_column('C:C', 10)

for i in range(len(samsung.Open)):
    worksheet.write('A%d'%(i+1),'%d'%samsung.Open[i])
    worksheet.write('B%d'%(i+1),'%d'%moveavg5[i])
    worksheet.write('C%d'%(i+1),'%d'%moveavg20[i])
    
workbook.close()


#plot
plt.plot(samsung.index, samsung.Open, 'b', label='Samsung Electronics')
plt.plot(list(samsung.index), moveavg5, 'r', label='Samsung Electronics')
plt.plot(list(samsung.index), moveavg20, 'y', label='Samsung Electronics')
plt.scatter(list(samsung.index), list(map(visual, buyindex.values())), c='b', s=0.5)
plt.scatter(list(samsung.index), list(map(visual, sellindex.values())), c='r', s=0.5)
plt.xlabel('days')
plt.ylabel('price')
plt.text(samsungindex[1],10000,'buyindex', fontdict={'color':'blue'})
plt.text(samsungindex[1],15000,'sellindex', fontdict={'color':'red'})
plt.title('overall graph')

plt.show()
