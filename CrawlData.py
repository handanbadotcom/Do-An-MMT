import requests
import lxml
import pandas
from bs4 import *
from datetime import date

#link web
url= 'https://sbv.gov.vn/TyGia/faces/TyGiaMobile.jspx?_afrLoop=14339020310096506&_afrWindowMode=0&_adf.ctrl-state=1786p90txj_21'

#tao ket noi va tao soup
r = requests.get(url).content
soup = BeautifulSoup(r,'lxml')

#chon bang can trich du lieu
allTables = soup.find_all('table',class_='jrPage')
table = allTables[1]

#lay data can thiet
rawData=[]
for td in table.find_all('td'):
    if td.text!='' and td.text!=' ':
        rawData.append(td.text)

Data=[]
for data in rawData:
    a = data.replace(data[0]+data[1],data[1])
    Data.append(a)

#tach data thanh cac truong du lieu khac nhau
#ten truong
Title=[]
#so thu tu
STT=[]
#ma ngoai te (USD,EUR,...)
NT=[]
#ten ngoai te
Ten_NT=[]
Mua=[]
Ban=[]
index=1

for i in range(1,6):
    Title.append(Data[index])
    index += 1
#đổi lại tên cột thành ko dấu đễ dễ thực hiện
Title[0] = 'STT'
Title[1] = 'Ngoai te'
Title[2] = 'Ten ngoai te'
Title[3] = 'Mua'
Title[4] = 'Ban'

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

#chuyen thanh data frame
Struct = {Title[0]:pandas.Series(STT),
          Title[1]:pandas.Series(NT),
   #       Title[2]:pandas.Series(Ten_NT), #có dấu bị lỗi
          Title[3]:pandas.Series(Mua),
          Title[4]:pandas.Series(Ban),}


DF = pandas.DataFrame(Struct)
print(DF)
JS = DF.to_json()
print(JS)

time = date.today()
filename = time.strftime("%d_%m_%Y")+".json"
with open(filename, "w") as outfile:
    outfile.write(JS)
