import mysql.connector

# MySQL Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="uticon"
)
mycursor = mydb.cursor()

sql = "SELECT * FROM `search` where timestampdiff(DAY, time, now()) >= 5"
mycursor.execute(sql)
exceedingSearchResult = list(mycursor.fetchall())

if (len(exceedingSearchResult) > 0):
    for x in exceedingSearchResult:
        sql2 = "DELETE FROM `search_result` where search_id=%s"
        mycursor.execute(sql2, (x[0],))
        mydb.commit()
        
        sql3 = "DELETE FROM `search` where id=%s"
        mycursor.execute(sql3, (x[0],))
        mydb.commit()     

# Select all search
sql4 = "SELECT s.*, timestampdiff(DAY, time, now()) as diff FROM `search` as s where timestampdiff(DAY, time, now()) < 5"
mycursor.execute(sql4)
searchResult = list(mycursor.fetchall())

print(searchResult)

countInvertDateArr = []
totalCount = 0
totalInvert = 0
# [id, count, invert]
for x in searchResult:
    invert = 5 - int(x[4])
    totalInvert += invert
    totalCount += int(x[2])
    countInvertDateArr.append([int(x[0]), int(x[2]), invert])

print("total count", totalCount, "total invert", totalInvert)

countInvertDateArr.sort(key=lambda x: (x[2], x[1]), reverse= True)

print(countInvertDateArr)

recommendation = []
for x in countInvertDateArr:
    recomAmount = round(((x[1] / totalCount) + (x[2] / totalInvert)) / 2 * 15)
    sql5 = "SELECT p.* FROM search_result sr inner join product p on sr.product_id = p.id where sr.search_id=%s order by sr.priority limit %s"
    mycursor.execute(sql5, (x[0], recomAmount))
    print(x[0], recomAmount)
    recommendation.extend(list(mycursor.fetchall()))

if (len(recommendation) < 15):
    randomCount = 15 - len(recommendation)
    sql6 = "SELECT * FROM product ORDER BY RAND() LIMIT %s"
    mycursor.execute(sql6, (randomCount,))
    recommendation.extend(list(mycursor.fetchall()))

# =========================================================================================================
# Print Result
# =========================================================================================================
# Delete targeted txt file
target = "searchresult.txt"
f = open(target, "r+")
f.truncate(0)
f.close()

# Write targeted txt file
for x in recommendation:
    with open(target, 'a', encoding='utf-8') as f:
        f.write(str(x[0][2]))
        f.write('\n')
        f.write(str(x[0][3]))
        f.write('\n')
        f.write(str(x[1]))
        f.write('\n')
        f.write('\n')