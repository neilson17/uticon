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
from bing_image_urls import bing_image_urls

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="uticon"
)
cursor = db.cursor()

for i,row in modified.iterrows():
    url = bing_image_urls(row["Product Name"], limit=1)
    
    row["Image"] = url[0]  if len(url) > 0 else "no"
    
    sql = "INSERT INTO `product` (`id`, `url`, `name`, `description`, `list_price`, `sale_price`, `brand`, `category`, `available`, `image`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, tuple(row))
    db.commit()

db.close()