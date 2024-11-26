#cmd
#pip install pandas,yfinace,matplotlib,xlsxwriter

from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import xlsxwriter


yf.pdr_override()


#stock class
class finance:
    def __init__(self):
        self.stock = 0
        self.stockmoney = 0
    def mainfunc(self,num):
        self.main=pdr.get_data_yahoo('00%d.KS'%num, start='2020-07-01', end='2021-07-01') #005930

      
#money, stock
money=100000000 #1억

def sumdev(k):
    return 0.5


#output
n=int(input("How many stocks would you do? "))
listen=[]
k=1       

for i in range(n):
    listen.append(chr(k))
    k+=1
for sam in listen:
    sam=finance()
    print("Enter the serial numbers of the stock")
    b=int(input())
    sam.mainfunc(b)
    print(sam.main)
    print(sam.main.index)
    print(sam.main.columns)  #date



#이동평균선

    #5일선
    open = list(sam.main.Open)
    moveavg5 = []
    for i in range(4):
        moveavg5.append(0)
    for i in range(4,len(open)):
        avg5 = 0
        a = 0
        for k in range(0,5):
            a += open[i-k]
        avg5 = a/5
        moveavg5.append(avg5)
    print(moveavg5)


    #20일선
    moveavg20 = []
    for i in range(19):
        moveavg20.append(0)
    for i in range(19,len(open)):
        avg20 = 0
        a = 0
        for k in range(0,20):
            a += open[i-k]
        avg20 = a/20
        moveavg20.append(avg20)
    print(moveavg20)


#5,20 이동평균선 알고리즘
    
    #1. 매수조건 (첫날에는 구매하지 않음)
    for i in range(21,len(open)):
        if open[i] > open[i-1] and open[i] > moveavg5[i] and moveavg5[i] > moveavg20[i] and money > open[i]:
            sam.stockmoney += int(0.5*money/open[i])
            money -= sam.stockmoney*open[i]
    #2. 매도조건
        if moveavg5[i] <= moveavg20[i] and money > 0:
            money += sam.stockmoney*open[i]
        sam.stockmoney = 0
        print("처음돈 100000000","나중돈 %d"%money)
#exel
    workbook = xlsxwriter.Workbook('stock.xlsx')
    worksheet = workbook.add_worksheet()

    cell_format = workbook.add_format({'border': 1})
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 10)

    for i in range(len(sam.main.Open)):
        worksheet.write('A%d'%(i+1),'%d'%sam.main.Open[i])
        worksheet.write('B%d'%(i+1),'%d'%moveavg5[i])
        worksheet.write('C%d'%(i+1),'%d'%moveavg20[i])
    
    workbook.close()


#plot
    plt.plot(sam.main.index, sam.main.Close, 'b', label='Samsung Electronics')
    plt.plot(list(sam.main.index), moveavg5, 'r', label='Samsung Electronics')
    plt.plot(list(sam.main.index), moveavg20, 'y', label='Samsung Electronics')

    plt.show()
        
