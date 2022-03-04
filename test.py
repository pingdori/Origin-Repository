from flask import *
import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
import os
# app=Flask(__name__)
# app.config["JSON_AS_ASCII"]=False
# app.config["TEMPLATES_AUTO_RELOAD"]=True
load_dotenv()
MYSQL_HOST=os.getenv("mysql_host")
MYSQL_PORT=os.getenv("mysql_port")
MYSQL_USER=os.getenv("mysql_user")
MYSQL_PASSWORD=os.getenv("mysql_password")
# keyword_query = request.args.get('keyword')
# connection = mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
# cursor = connection.cursor()
# cursor.execute("USE `taipei-attractions`")
# cursor.execute("SELECT JSON_OBJECT('id',`id`,'name',`name`,'category',`category`,'description',`description`,'address',`address`,'transport',`transport`,'mrt',`mrt`,'latitude',`latitude`,'longitude',`longitude`) FROM `data` WHERE `name` like '%溫泉%' ")
# print(img)
# cursor.execute("SELECT JSON_OBJECT('id',`id`,'name',`name`,'category',`category`,'description',`description`,'address',`address`,'transport',`transport`,'mrt',`mrt`,'latitude',`latitude`,'longitude',`longitude`) FROM `data` WHERE `name` like '%溫泉%' ")

# cursor.execute("SELECT `name`,`images` FROM `data_images` WHERE `name` like '%溫泉%' ")
# imgResults = cursor.fetchall()
# for d in imgResults:
#         allImg=str(d[1])
        # data = '{"data":"'+name+'"}'
# s="SELECT JSON_OBJECT('id',`id`,'name',`name`,'username',`username`) FROM `member` WHERE `username` = %s " ,(username_query,)

connection = mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
cursor = connection.cursor()
cursor.execute("USE `taipei-attractions`")
ff=[11]
count="SELECT count(*) from `data` where `name` like '%園%'"
cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name`=`data_images`.`name` LIMIT %s",(ff))
# cursor.description("SELECT * from `data`")
# cursor.execute("SELECT * FROM `data_images` WHERE `name` like '%溫泉%' ")
"SELECT count(*) from `data`"
results = cursor.fetchall()
a=json.dumps(results)
b=json.loads(a) 
c=cursor.description
p=json.dumps(c)
l=json.loads(p) 
de=[desValue[0] for desValue in l]
d=["id","name","category","description","address","transport","mrt","latitude","longitude","images"]

allFields=cursor.description
sum=0

dic=dict()
for value in b:

        ID=["id"]
        name=["name"]
        category=["category"]
        description=["description"]
        address=["address"]
        transport=["transport"]
        mrt=["mrt"]
        latitude=["latitude"]
        longitude=["longitude"]
        images=["images"]
        # dic[ID[0]]=int(value[0])
        # dic[name[0]]=str(value[1])
        # dic[category[0]]=str(value[2])
        # dic[description[0]]=str(value[3])
        # dic[address[0]]=str(value[4])
        # dic[transport[0]]=str(value[5])
        # dic[mrt[0]]=str(value[6])
        # dic[latitude[0]]=str(value[7])
        # dic[longitude[0]]=str(value[8])
        # dic[images[0]]=str(value[9])
        ID.append(int(value[0]))
        
        # print(value)

for i in b:
        b=dict(zip(d,b))
        x=["data"]
        v=dict(zip(x,b))
        print (v)
# for i in b:
#     allId=str(i[0])
#     Id='"id":'+ allId +","
    
#     allName=str(i[1])
#     name='"name":'+ allName +","
    
#     allCategory=str(i[2])
#     category='"Category":'+allCategory+","

#     allDescription=str(i[3])
#     description='"Description":'+ allDescription+","
    
#     allAddress=str(i[4])
#     address='"Address":'+allAddress+","

#     allTransport=str(i[5])
#     transport='"Transport":'+allTransport+","

#     allMrt=str(i[6])
#     mrt='"mrt":'+allMrt+","

#     allLatitude=str(i[7])
#     latitude='"latitude":'+allLatitude+","

#     AllLongitude=str(i[8])
#     longitude='"longitude":'+AllLongitude+","

#     allImg=str(i[11])
#     img='"longitude":'+allImg+","
#     nextPage="ddd"
#     data="[{"+Id+name+category+description+address+transport+mrt+latitude+longitude+img+"}],"
#     j='{"data":'+data+"}"
    
# x=cursor.execute(count)
# c=cursor.fetchone()
# for x in c:

#     test=int(c[0])
#     a=str(test+1)
#     p="adsasd"+a


cursor.close()
connection.close()
    # if test >=11:
    #     page=
    # tests="co"+test
    
