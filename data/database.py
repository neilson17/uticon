# ==========================================================================
# Get the data from CSV
# ==========================================================================
import pandas as pd

file = "data.csv"
csvFile = pd.read_csv(file)
csvFile.drop('Crawl Timestamp', inplace=True, axis=1)
csvFile.drop('Item Number', inplace=True, axis=1)
csvFile.drop('Gtin', inplace=True, axis=1)
csvFile.drop('Package Size', inplace=True, axis=1)
csvFile.drop('Postal Code', inplace=True, axis=1)

modified = csvFile.dropna()
modified["Available"] = modified["Available"].astype(int)

# ==========================================================================
# Processing data to database
# ==========================================================================
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="uticon"
)
mycursor = mydb.cursor()

for i,row in modified.iterrows():
    sql = "INSERT INTO `product` (`id`, `url`, `name`, `description`, `list_price`, `sale_price`, `brand`, `category`, `available`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, tuple(row))
    mydb.commit()

mydb.close()