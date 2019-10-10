
toDatabaseID = {
    'allrecipes' : 'AR' #key : value
}


url = 'https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/'
info = url.split('/')
name = info[2].split('.')[1]
ID = info[4]
if(name in toDatabaseID):  #does this ignore case??? ANS: Not yet
    databaseID = str(toDatabaseID.get(name))+str(ID)
else: 
    databaseID = str(name) + str(ID)
print(databaseID)
