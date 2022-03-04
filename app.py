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
	# try:
	keyword_query = request.args.get('keyword')
	pageStrquery= str(request.args.get('page'))
	
	if 	pageStrquery and 	keyword_query ==None:
		
		connection = mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
		cursor = connection.cursor()
		cursor.execute("USE `taipei-attractions`")
				# selectKeyword="SELECT * from `data` Join `data_images` on `data`.`name`=`data_images`.`name` and `data`.`name` like %s LIMIT 11 OFFSET 0" ,(keyword_query,)
				# selectPage="SELECT * from `data` Join `data_images` on `data`.`name`=`data_images`.`name` and `data`.`name` LIMIT 11 OFFSET %s" ,(page_query,)
				# selectKeypage="SELECT * from `data` Join `data_images` on `data`.`name`=`data_images`.`name` and `data`.`name` like %s  LIMIT 11 OFFSET %s;" ,(keyword_query,page_query,)
		countAll="SELECT count(*) from `data`"
				# count="SELECT count(*) from `data` WHERE `name` like %s LIMIT 11 OFFSET %s",(keyword_query,page_query,)
				# if keyword_query ==None:
				# if pageStrquery==0:
				# 	pageOffset=0
				# else:
				# 	pageOffset=int(pageStrquery)*11
		ff=[11]
		cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name`=`data_images`.`name`")
		results = cursor.fetchall()
		jsonA=json.dumps(results)
		jsonB=json.loads(jsonA) 
		des=cursor.description
		desDumps=json.dumps(des)
		desLoad=json.loads(desDumps) 
		title=["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
			

		# dic=dict()
		# ID=["id"]
		# name=["name"]
		# category=["category"]
		# description=["description"]
		# address=["address"]
		# transport=["transport"]
		# mrt=["mrt"]
		# latitude=["latitude"]
		# longitude=["longitude"]
		# images=["images"]
		# sum=0
		# for value in jsonB:
			
		# 	while sum<len(value):
		# 		dic[ID[0]]=str(value[0])
		# 		dic[name[0]]=str(value[1])
		# 		dic[category[0]]=str(value[2])
		# 		dic[description[0]]=str(value[3])
		# 		dic[address[0]]=str(value[4])
		# 		dic[transport[0]]=str(value[5])
		# 		dic[mrt[0]]=str(value[6])
		# 		dic[latitude[0]]=str(value[7])
		# 		dic[longitude[0]]=str(value[8])
		# 		dic[images[0]]=str(value[9])
		# 		sum+=1
		# 		print(dic)
		# 		return(jsonify(dic))
		# dic=[]
		# dic1={}
		# ID="id"
		# name="name"
		# category="category"
		# description="description"
		# address="address"
		# transport="transport"
		# mrt="mrt"
		# latitude="latitude"
		# longitude="longitude"
		# images="images"
		# IID=desLoad[0]
		# for value in jsonB:
		# 	# while sum<len(value):
		# 		allId=str(value[0])
		# 		Id=ID[0]+ allId
		# 		json.dumps(Id)
				

		# 		# sum+=1
		# return(jsonify(Id))
		# except:
		# 	null = '{"data":null}'
		# 	return null
		# finally:
			# cursor.close()
			# connection.close()
					
			# elif page_query and keyword_query != None:
			# 	cursor.execute(selectKeypage)
				
			# cursor.execute("SELECT * from `data` Join `data_images` on `data`.`name`=`data_images`.`name` and `data`.`name` like %s  LIMIT 11 OFFSET %s;" ,(keyword_query,page_query,))
			# results = cursor.fetchall()
		list_data=[]
		for i in jsonB:
				co=dict(zip(title,jsonB))
				x=["data"]
				d1 = defaultdict(lambda: defaultdict(dict))
				list_data.append(co)
				d1["data"]=list_data
	return(jsonify(d1))
app.debug = True
app.run(port=3000)