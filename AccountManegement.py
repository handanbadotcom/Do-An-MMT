import pandas as pd
import json
#khoi tao file cho lan dau chay code
def initAccountFile(tenFile):
    struct = {'ID':pd.Series(''),
          'pass':pd.Series('')}
    DF = pd.DataFrame(struct)
    with open(tenFile, 'w+') as file:
        DF.to_json(file, orient='index')
#Kiem tra da co tai khoan chua, neu co roi la True
def checkAccount(fileName, ID):
    with open(fileName) as json_file:
        DF = pd.read_json(json_file, orient='index')
    n = int(DF.size /2)
    for i in range(0,n):
        if DF.iat[i,0] == ID:
            return True
    return False
#them tai khoan vao file
def addAccount(fileName, ID, pw):
    with open(fileName) as json_file:
        DF = pd.read_json(json_file, orient='index')
    n = int(DF.size /2)
    struct = {'ID':pd.Series(ID,index = [n]),
          'pass':pd.Series(pw,index= [n])}
    newDF = pd.DataFrame(struct)
    DF = pd.concat([DF, newDF], axis=0, join='inner')
    with open(fileName, 'w+') as file:
        DF.to_json(file, orient='index')
#kiem tra pass validation
def pw_check(pw):
      
    SpecialSym =['!', '@', '#', '$', '%', '^', '&', '*']
    val = True
    level = 0  
    if len(pw) < 6:
        print('length should be at least 6')
        return False
          
    if len(pw) > 20:
        print('length should be not be greater than 20')
        return False
          
    if any(char.isdigit() for char in pw):
        level += 1
          
    if any(char.isupper() for char in pw):
        level += 1
          
    if any(char.islower() for char in pw):
        level += 1
          
    if any(char in SpecialSym for char in pw):
        level += 1

    if level < 3:
        val = False
        print('Password should have at least 3 of things: numberal, uppercase, lowercase letter, special symbol(!, @, #, $, %, ^, &, *)!!!')
    return val
  
#initAccountFile('test.json')

with open('test.json') as json_file:
        DF = pd.read_json(json_file, orient='index')
        print(DF)
ID = 'huy'
pw = '2412'
if pw_check(pw):
    print('pass is valid!!!')
if checkAccount('test.json', ID) == True:
    print('tai khoan da ton tai!!!')
else:
    addAccount('test.json', ID, pw)
    print('da tao tai khoan!!!')