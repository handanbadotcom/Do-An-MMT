import pandas

data = pandas.read_json('test.json') #đọc vào file json
find= 'EUR' #tên ngoại tệ
#f =data[data['Ngoai te'].str.contains('USD')] # xuất ra thông tin ngoại tệ

def search_currency(data, find):
    for i in data:
        if data[i]["Ngo\u1ea1i t\u1ec7"]==find:
            print(data[i])

def search_date(data, month, date, year):
    date = str(month)+'/'+str(date)+'/'+str(year)
    for i in data:
        if data[i]["Ng\u00e0y"]==date:
            print(data[i])


search_currency(data,'USD')
search_date(data,12,19,2021)




