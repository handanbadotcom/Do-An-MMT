import pandas

data = pandas.read_json('Data.json') #đọc vào file json
find= 'EUR' #tên ngoại tệ
f =data[data['Ngoai te'].str.contains('USD')] # xuất ra thông tin ngoại tệ
print(f)





