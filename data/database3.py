# ==========================================================================
# Processing data to database
# ==========================================================================
import mysql.connector
from bing_image_urls import bing_image_urls

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="uticon"
)
cursor = db.cursor()

sql = "SELECT * FROM PRODUCT"
cursor.execute(sql)
result = list(cursor.fetchall())
# checkpoint 1 -> 2553
# checkpoint 2 -> 9560
for i in range(2553, len(result)):
    print(i)
    if (result[i][9] == None):
      url = bing_image_urls(result[i][2], limit=1) 
      imageurl = url[0] if len(url) > 0 else "no"
      
      sql2 = "UPDATE `product` set image=%s where id=%s"
      cursor.execute(sql2, (imageurl, result[i][0]))
      db.commit()

db.close()