# MySQL Connection
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="uticon"
)
mycursor = mydb.cursor()

# Define Keyword
keyword = "lifeway organic"

# Search in the database
from nltk.tokenize import word_tokenize
words = word_tokenize(keyword.lower())
# name like query
resultRaw = []
for w in words:
    keyword = "%" + w + "%"
    sql = "SELECT * FROM products where name like %s or description like %s"
    mycursor.execute(sql, (keyword, keyword))
    resultRaw.extend(list(mycursor.fetchall()))


i = 0

resultRaw = resultRaw[:7]

res = []
for x in resultRaw:
    # print(x[0])
    if resultRaw.count(x)>1:
        if x not in res:
             res.append(x)
    else:
        res.append(x)

for x in res:
    print(x[0])
# for x in range(10):
    # print(resultRaw[x][0])

for x in resultRaw:
    # print(x[0], x[2])
    # for i in my_list:
    #  if my_list.count(i)>1:
    #      if i not in duplicates:
    #          duplicates.append(i)
    # with open('coba.txt', 'a', encoding='utf-8') as f:
        # f.write(str(x[0]))
        # f.write(str(x[0][2]))
        # f.write('\n')
        # f.write(str(x[0][3]))
        # f.write('\n')
        # f.write(str(x[1]))
        # f.write('\n')
    i+=1
    if i == 10:
        break