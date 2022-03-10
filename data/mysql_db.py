import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
import os

# load_dotenv()
# MYSQL_HOST = os.environ.get("mysql_host")
# MYSQL_PORT = os.environ.get("mysql_port")
# MYSQL_USER = os.environ.get("mysql_user")
# MYSQL_PASSWORD = os.environ.get("mysql_password")

# connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
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
    Mrt=i["MRT"]
    latitude=i["latitude"]
    longitude=i["longitude"]
    imgFile=i["file"]
    urlSplit=imgFile.split("https")
    strA=",https".join(urlSplit)
    
    strB=strA.split(",")
    strB.pop(0)
    
    filterData=str([a for a in strB if ".jpg" in a or ".JPG" in a])
    splitB=filterData.split("[")
    splitC=splitB[1].split("]")
    # splitD=splitC.split("'")
    print(urlSplit)
    # for i in filterData:
    #     images=str(filterData[i])
    # cursor.execute("INSERT INTO `data`(`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(name,category,description,address,transport,Mrt,latitude,longitude,))
    cursor.execute("INSERT INTO `data_images`(`name`,`images`) VALUES(%s,%s)",(name,splitC[0],))
    connection.commit()
    # cursor.close()
    # connection.close()
