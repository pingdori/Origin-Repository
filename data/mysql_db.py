import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
import os

load_dotenv()
MYSQL_HOST=os.getenv("mysql_host")
MYSQL_PORT=os.getenv("mysql_port")
MYSQL_USER=os.getenv("mysql_user")
MYSQL_PASSWORD=os.getenv("mysql_password")

connection = mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
cursor = connection.cursor()
cursor.execute("USE `taipei-attractions`")
results = cursor.fetchall()
with open('taipei-attractions.json',encoding='utf-8') as f:
    jsonData=json.load(f)
dataList=jsonData["result"]["results"]
for i in dataList:
    name=i["stitle"]
    category=i["CAT2"]
    description=i["xbody"]
    addr=i["address"]
    address=addr.replace(" ", "")
    transport=i["info"]
    MRT=i["MRT"]
    latitude=i["latitude"]
    longitude=i["longitude"]
    imgFile=i["file"]
    urlSplit=imgFile.split("https")
    strA=",https".join(urlSplit)
    strB=strA.split(",")
    strB.pop(0)
    
    filterData=[a for a in strB if ".jpg" in a or ".JPG" in a]
    images=",".join(filterData)
    
    cursor.execute("INSERT INTO `data`(`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,)",(name,category,description,address,transport,MRT,latitude,longitude,))
    cursor.execute("INSERT INTO `data`(`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,category,description,address,transport,MRT,latitude,longitude))
    cursor.execute("INSERT INTO `data_images`(`name`,`images`) VALUES(%s,%s)",(name,images,))
    connection.commit()
    cursor.close()
    connection.close()
