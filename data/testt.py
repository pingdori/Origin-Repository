
import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
import os
connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
cursor  =  connection.cursor()
cursor.execute("USE `taipei-attractions`")
countAll  =  "SELECT count(*) from `data`"
cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` order by `data`.`id` ")
results  =  cursor.fetchall()
jsonA  =  json.dumps(results)
jsonB = json.loads(jsonA) 
des = cursor.description
desDumps = json.dumps(des)
desLoad = json.loads(desDumps) 
title = ["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
title0 = ["data"]
a=jsonB[0]
listDataA= []
listDataB=[]
dic = dict()
for i in range(len(jsonB)):
	dictCombin = dict(zip(title,jsonB[i]))
	listDataA.append(dictCombin)
	dic[title0[0]] = listDataA
				
	allimages=dic['data'][i]['images']
	splitA=allimages.split(",")
	splitB=splitA[0].split("[")
	splitC=splitB[1].split("'")
	listDataB.append(splitC[1])
	dic['data'][i]['images']=listDataB
	strA=str(dic['data'][i])
	a=dic['data'][i]
	dic[title0[0]]=a
				# results='{data:'+strA+"}"
				# d=json.loads(results)
print(dic)