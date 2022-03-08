from flask import *
import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
from collections import defaultdict
import os
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
# load_dotenv()
# MYSQL_HOST = os.environ.get("mysql_host")
# MYSQL_PORT = os.environ.get("mysql_port")
# MYSQL_USER = os.environ.get("mysql_user")
# MYSQL_PASSWORD = os.environ.get("mysql_password")
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
		keywordQuery  =  request.args.get('keyword',None)
		pageStrquery  =  str(request.args.get('page'))
		if pageStrquery ==  None:
			connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
			# connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
			cursor  =  connection.cursor()
			cursor.execute("USE `taipei-attractions`")
			countAll  =  "SELECT count(*) from `data`"
			cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` order by `data`.`id` LIMIT 12")
			results  =  cursor.fetchall()
			jsonA  =  json.dumps(results)
			jsonB = json.loads(jsonA) 
			des = cursor.description
			desDumps = json.dumps(des)
			desLoad = json.loads(desDumps) 
			title = ["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
			title0 = ["nextpage","data"]
			listData = []
			dic = dict()
			for i in range(len(jsonB)):
				dictCombin = dict(zip(title,jsonB[i]))
				listData.append(dictCombin)
				dic[title0[1]] = listData
				dic[title0[0]] = 1	
			return(jsonify(dic))
			cursor.close()
			connection.close()
		pageQuery = int(request.args.get('page',0))
		if keywordQuery == None: 	
			if pageQuery  ==  0 :
				connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
				# connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
				cursor  =  connection.cursor()
				cursor.execute("USE `taipei-attractions`")
				countAll = "SELECT count(*) from `data`"
				cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` order by `data`.`id` LIMIT 12")
				results  =  cursor.fetchall()
				jsonA = json.dumps(results)
				jsonB = json.loads(jsonA) 
				des = cursor.description
				desDumps = json.dumps(des)
				desLoad = json.loads(desDumps) 
				title = ["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
				ID = ["nextpage","data"]
				title0 = ["nextpage","data"]
				listData = []
				dic = dict()
				for i in range(len(jsonB)):
						dictCombin = dict(zip(title,jsonB[i]))
						listData.append(dictCombin)
						dic[title0[1]] = listData
						dic[title0[0]] = 1
				return(jsonify(dic))
				cursor.close()
				connection.close()
			elif pageQuery > 0:
				connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
				# connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
				cursor  =  connection.cursor()
				cursor.execute("USE `taipei-attractions`")
				countAll = "SELECT count(*) from `data`"
				cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` LIMIT 12 ")
				results  =  cursor.fetchall()
				jsonA = json.dumps(results)
				jsonB = json.loads(jsonA) 
				title = ["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
				cursor.execute(countAll)
				result = cursor.fetchone()
				a = int(result[0])//12
				title0 = ["nextpage","data"]
				if pageQuery < a+1:
					nextpageOffset = 12*pageQuery
					cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` LIMIT 12 OFFSET %s",(nextpageOffset,))
					nextpageResults = cursor.fetchall()
					jsonC = json.dumps(nextpageResults)
					jsonD = json.loads(jsonC) 
					listData0 = []
					dic0 = dict()
					for i in range(len(jsonD)):
						dictCombin0 = dict(zip(title,jsonD[i]))
						listData0.append(dictCombin0)
						dic0[title0[1]] = listData0
						if pageQuery<= a-1:
							page1 = pageQuery+1
							dic0[title0[0]] = page1
						elif pageQuery >a-1:
							page1 = "null"
							dic0[title0[0]] = page1	
					return(jsonify(dic0))
					cursor.close()
					connection.close()
				elif pageQuery >=  a+1:	
					title1 = []
					dic1 = dict()
					dic1[title0[1]] = []
					dic1[title0[0]] = "null"
				return(jsonify(dic1))
				cursor.close()
				connection.close()
		if keywordQuery != None :
			connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
			# connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
			cursor  =  connection.cursor()
			cursor.execute("USE `taipei-attractions`")
			cursor.execute("SELECT count(*)  `name`from `data` where `name` like '%"+request.args.get('keyword',None)+"%' order by `data`.`id`;")
			result = cursor.fetchone()
			a=int(result[0])
			y = int(result[0])//12
			b = int(result[0]) % 12
			if  a> 12 :
				nextpageOffset = 12*pageQuery
				cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` and `data`.`name` like '%"+request.args.get('keyword',None)+"%' order by `data`.`id` LIMIT 12 OFFSET %s",(nextpageOffset,))
				results  =  cursor.fetchall()
				jsonA = json.dumps(results)
				jsonB = json.loads(jsonA) 
				des = cursor.description
				desDumps = json.dumps(des)
				desLoad = json.loads(desDumps) 
				title = ["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
				title0 = ["nextpage","data"]
				listData = []
				dic = dict()
				if 12 > b >0:
					if pageQuery > y:
						dic0=dict()
						dic0[title0[1]] = []
						dic0[title0[0]] = "null"	
						return(jsonify(dic0))
					else:	
						for i in range(len(jsonB)):
							dictCombin = dict(zip(title,jsonB[i]))
							listData.append(dictCombin)
							dic[title0[1]] = listData
							if pageQuery < y:
								page1 = pageQuery+1
								dic[title0[0]] = page1
							elif pageQuery == y:
								page1 = "null"
								dic[title0[0]] = page1
						return(jsonify(dic))
						cursor.close()
						connection.close()
				elif b == 0 :
					for i in range(len(jsonB)):
							dictCombin = dict(zip(title,jsonB[i]))
							listData.append(dictCombin)
							dic[title0[1]] = listData
							if pageQuery< y-1:
								page1 = pageQuery+1
								dic[title0[0]] = page1
							elif pageQuery == y-1:
								page1 = "null"
								dic[title0[0]] = page1
							elif pageQuery > y-1:
								dic[title0[1]] = []
								dic[title0[0]] = "null"		
					return(jsonify(dic))
					cursor.close()
					connection.close()
			elif 0< a <12:
				cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` and `data`.`name` like '%"+request.args.get('keyword',None)+"%' order by `data`.`id` LIMIT 12")
				results  =  cursor.fetchall()
				jsonA = json.dumps(results)
				jsonB = json.loads(jsonA) 
				des = cursor.description
				desDumps = json.dumps(des)
				desLoad = json.loads(desDumps) 
				title = ["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
				ID = ["nextpage","data"]
				title0 = ["nextpage","data"]
				listData = []
				dic = dict()
				for i in range(len(jsonB)):
					if  pageQuery < 1:
						dictCombin = dict(zip(title,jsonB[i]))
						listData.append(dictCombin)
						dic[title0[1]] = listData
						page0 = "null"
						dic[title0[0]] = page0
					elif pageQuery >= 1:
						dic[title0[1]] = []
						dic[title0[0]] = "null"
				return(jsonify(dic))
				cursor.close()
				connection.close()
			elif a == 0 :
				dic1 = dict()
				dic1[title0[1]] = []
				dic1[title0[0]] = "null"
				return(jsonify(dic1))
				cursor.close()
				connection.close()
	except:
		errorTitle = ["error","message"]
		dic1 = dict()
		dic1[errorTitle[0]] = "true"
		dic1[errorTitle[1]] = "error"
		return(jsonify(dic1))


@app.route("/api/attractions/<int:id>")
def attractionID(id):
	try:
		connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
		# connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
		cursor  =  connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		cursor.execute("SELECT `data`.`id`,`data`.`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` and `data`.`id` like %s ",(id,))
		results  =  cursor.fetchall()
		jsonA = json.dumps(results)
		jsonB = json.loads(jsonA) 
		des = cursor.description
		desDumps = json.dumps(des)
		desLoad = json.loads(desDumps) 
		title = ["id","name","category","description","address","transport","mrt","latitude","longitude","images"]
		if id <=  58 :
			title0 = ["nextpage","data"]
			listData = []
			dic = dict()
			for i in range(len(jsonB)):
				dictCombin = dict(zip(title,jsonB[i]))
				listData.append(dictCombin)
				dic[title0[1]] = listData
				page0 = "null"
				dic[title0[0]] = page0	
			return(jsonify(dic))
		elif id>58 :
			errorTitle = ["error","message"]
			dic1 = dict()
			dic1[errorTitle[0]] = "true"
			dic1[errorTitle[1]] = "error"
			return(jsonify(dic1))
			cursor.close()
			connection.close()
	except:
		errorTitle = ["error","message"]
		dic1 = dict()
		dic1[errorTitle[0]] = "true"
		dic1[errorTitle[1]] = "error"
		return(jsonify(dic1))
app.run(host='0.0.0.0',port=3000)