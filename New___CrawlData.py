import requests
import lxml
import pandas
from bs4 import *
import json
from datetime import *
import datetime
NUM_OF_DAY = 3 #so ngay toi da cua file json
#link web
url = 'https://sbv.gov.vn/TyGia/faces/TyGiaMobile.jspx?_afrLoop=14339020310096506&_afrWindowMode=0&_adf.ctrl-state=1786p90txj_21'

def initJsonFile(tenFile, NumOfDay):  #Khoi tao file JSON du lieu trong voi so ngay cho truoc
    sotmp = []
    chutmp = []
    STT = [1,2,3,4,5,6,7]
    NT = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'AUD', 'CAD']
    TenNT = ['Do la My','Dong Euro','Yen Nhat', 'Bang Anh', 'Pho rang Thuy Si', 'Do la Uc', 'Do la Canada']
    for i in range(0, 7*NumOfDay):
        sotmp.append(0)
        chutmp.append('a')
    Struct = {'Ngày'         : pandas.Series(chutmp),
              'STT'          : pandas.Series(STT * NumOfDay),
              'Ngoại tệ'     : pandas.Series(NT * NumOfDay),
              'Tên Ngoại tệ' : pandas.Series(TenNT * NumOfDay),
              'Mua'          : pandas.Series(sotmp),
              'Bán'          : pandas.Series(sotmp),}
    DF = pandas.DataFrame(Struct)
    with open(tenFile, 'w+') as file:
        DF.to_json(file, orient='index')
def updateFile(fileName, NumOfDay, Ban, Mua):
    with open(fileName) as json_file:
        data = pandas.read_json(json_file, orient='index')
    now = datetime.datetime.now()
    today=now.strftime("%m/%d/%Y")
    if(data.iat[7 * NumOfDay - 1, 0] != today):    #data of new day
        #push up data for new day
        for i in range(0, 7 * (NumOfDay - 1)):
            for j in range(0, 6):
                data.iat[i, j] = data.iat[i + 7, j]
        #replace data of column day
        for i in range(-7, 0):
            data.iat[i, 0] = today
    for i in range(-7, 0):
        data.iat[i,4] = Mua[i]
        data.iat[i,5] = Ban[i]
    #print(data)
    with open(fileName, 'w+') as file:
        data.to_json(file, orient='index')

def updateData(url, fileName, NumOfDay):
    #tao ket noi va tao soup
    r = requests.get(url).content
    soup = BeautifulSoup(r,'lxml')

    #chon bang can trich du lieu
    allTables = soup.find_all('table', class_='jrPage')
    table = allTables[1]

    #lay data can thiet
    rawData = []
    for td in table.find_all('td'):
        if td.text != '' and td.text != ' ':
            rawData.append(td.text)

    Data = []
    for data in rawData:
        a = data.replace(data[0]+data[1], data[1])
        Data.append(a)

    Title = []  #ten truong
    STT = []    #so thu tu  
    NT = []     #ma ngoai te (USD,EUR,...)    
    Ten_NT = [] #ten ngoai te
    Mua = []    #Gia mua
    Ban = []    #Gia ban
    index = 1

    #tach data thanh cac truong du lieu khac nhau
    for i in range(1,6):
        Title.append(Data[index])
        index += 1
    for i in range(1,8):
        STT.append(Data[index])
        index += 1
        NT.append(Data[index])
        index += 1
        Ten_NT.append(Data[index])
        index += 1
        Mua.append(Data[index])
        index += 1
        Ban.append(Data[index])
        index += 1
    #Ghi du lieu da moi vao file
    updateFile(fileName, NumOfDay, Ban, Mua)
initJsonFile('test.json',NUM_OF_DAY)
updateData(url, 'test.json', NUM_OF_DAY)
with open('test.json') as json_file:
        data = pandas.read_json(json_file, orient='index')
print(data)