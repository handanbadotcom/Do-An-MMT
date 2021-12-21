import pandas

data = pandas.read_json('test.json') #đọc vào file json
find= 'EUR' #tên ngoại tệ
#f =data[data['Ngoai te'].str.contains('USD')] # xuất ra thông tin ngoại tệ

def search_currency(data, find):
    f=''
    for i in data:
        if data[i]["Ngo\u1ea1i t\u1ec7"]==find:  
          f=f+str(data[i].map(str))
          f=f+'\n'
    return(f)

def search_date(data, date):
    f=''
    for i in data:
        if data[i]["Ng\u00e0y"]==date:
            f=f+str(data[i].map(str)) #print(data[i])
            f=f+ '\n'
    return(f)
def search(data, currency=None, date=None):
    f=''
    if date==None:
      return ( search_currency(data,currency))
    if currency==None:
        return(search_date(data,date))
    else:    
        for i in data:
            if (data[i]["Ngo\u1ea1i t\u1ec7"]==currency) and (data[i]["Ng\u00e0y"]==date):
               f=f+data[i].map(str) # print(data[i])
    return(f)

#search_currency(data,'USD')
#search_date(data,12,19,2021)
print(search(data,date='12/21/2021'))




