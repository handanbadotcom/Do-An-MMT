import pandas

data = pandas.read_json('Data.json') #đọc vào file json
find= 'USD' #tên ngoại tệ
f =data[data['Ngoai te'].str.contains(find)] # xuất ra thông tin ngoại tệ
print(f)





