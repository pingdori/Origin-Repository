from flask import *
import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
from collections import defaultdict
import os
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
load_dotenv()
MYSQL_HOST=os.getenv("mysql_host")
MYSQL_PORT=os.getenv("mysql_port")
MYSQL_USER=os.getenv("mysql_user")
MYSQL_PASSWORD=os.getenv("mysql_password")
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
	
@app.route("/api/attractions")
	
def apiAttraction():
	try:
		pageStrquery= str(request.args.get('page'))
		if pageStrquery ==None:
			connection = mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
		cursor = connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		countAll="SELECT count(*) from `data`"
		cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name`=`data_images`.`name` order by `data`.`id` LIMIT 12")
		results = cursor.fetchall()
		jsonA=json.dumps(results)
		jsonB=json.loads(jsonA) 
		des=cursor.description
		desDumps=json.dumps(des)
		desLoad=json.loads(desDumps) 
		title=["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
		ID=["nextpage","data"]
		title0=["nextpage","data"]
		listData=[]
		dic=dict()
		for i in range(len(jsonB)):
			dictCombin=dict(zip(title,jsonB[i]))
			listData.append(dictCombin)
			dic[title0[1]]=listData
			page0=1
			dic[title0[0]]=page0	
		return(jsonify(dic))
		keyword_query = request.args.get('keyword')
		
		page_query=int(request.args.get('page'))
		if 	page_query == 0 :
			
			connection = mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
			cursor = connection.cursor()
			cursor.execute("USE `taipei-attractions`")
			countAll="SELECT count(*) from `data`"
			cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name`=`data_images`.`name` order by `data`.`id` LIMIT 12")
			results = cursor.fetchall()
			jsonA=json.dumps(results)
			jsonB=json.loads(jsonA) 
			des=cursor.description
			desDumps=json.dumps(des)
			desLoad=json.loads(desDumps) 
			title=["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
			ID=["nextpage","data"]
			title0=["nextpage","data"]
			listData=[]
			dic=dict()
			for i in range(len(jsonB)):
					dictCombin=dict(zip(title,jsonB[i]))
					listData.append(dictCombin)
					dic[title0[1]]=listData
					page0=1
					dic[title0[0]]=page0	
			return(jsonify(dic))
		elif page_query >0:
			connection = mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
			cursor = connection.cursor()
			cursor.execute("USE `taipei-attractions`")
			countAll="SELECT count(*) from `data`"
			cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name`=`data_images`.`name` LIMIT 12 ")
			results = cursor.fetchall()
			jsonA=json.dumps(results)
			jsonB=json.loads(jsonA) 
			title=["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
			cursor.execute(countAll)
			result=cursor.fetchone()
			a=int(result[0])//12
			b=int(result[0]) % 12
			title0=["nextpage","data"]
			if page_query < a+1:
				nextpageOffset=12*page_query
				cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name`=`data_images`.`name` LIMIT 12 OFFSET %s",(nextpageOffset,))
				nextpageResults=cursor.fetchall()
				jsonC=json.dumps(nextpageResults)
				jsonD=json.loads(jsonC) 
				listData0=[]
				dic0=dict()
				for i in range(len(jsonD)):
					dictCombin0=dict(zip(title,jsonD[i]))
					listData0.append(dictCombin0)
					dic0[title0[1]]=listData0
					if page_query<=a-1:
						page1=page_query+1
						dic0[title0[0]]=page1
					
					elif page_query >a-1:
						page1="null"
						dic0[title0[0]]=page1	
				return(jsonify(dic0))
				cursor.close()
				connection.close()
			elif page_query >= a+1:	
				title1=[]
				dic1=dict()
				dic1[title0[1]]=[]
				dic1[title0[0]]="null"
			return(jsonify(dic1))
			cursor.close()
			connection.close()
	except:
		r=requests.get("http://127.0.0.1:3000/api/attractions")
		if r.status_code == 400 or 500:
			errorTitle=["error","message"]
			dic1=dict()
			dic1[errorTitle[0]]="true"
			dic1[errorTitle[1]]="error"
			return(jsonify(dic1))

@app.route("/api/attractions/<int:id>")
def attractionID(id):
	try:
		cursor = connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		
		cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name`=`data_images`.`name` and `data`.`id` like %s ",(id,))
		results = cursor.fetchall()
		jsonA=json.dumps(results)
		jsonB=json.loads(jsonA) 
		des=cursor.description
		desDumps=json.dumps(des)
		desLoad=json.loads(desDumps) 
		title=["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
		ID=["nextpage","data"]

		title0=["nextpage","data"]
		listData=[]
		dic=dict()
		for i in range(len(jsonB)):
			dictCombin=dict(zip(title,jsonB[i]))
			listData.append(dictCombin)
			dic[title0[1]]=listData
			page0="null"
			dic[title0[0]]=page0	
		return(jsonify(dic))
	except:
		r=requests.get("http://127.0.0.1:3000/api/attractions/")
		if r.status_code == 400 or 500:
			errorTitle=["error","message"]
			dic1=dict()
			dic1[errorTitle[0]]="true"
			dic1[errorTitle[1]]="error"
			return(jsonify(dic1))
app.run(port=3000)