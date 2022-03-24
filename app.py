from flask import *
import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
from collections import defaultdict
from flask_cors import CORS
from pymysql import NULL
from werkzeug.security import generate_password_hash,check_password_hash
import os
from config import Config 
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
load_dotenv()
MYSQL_HOST = os.environ.get("mysql_host")
MYSQL_PORT = os.environ.get("mysql_port")
MYSQL_USER = os.environ.get("mysql_user")
MYSQL_PASSWORD = os.environ.get("mysql_password")
app.secret_key = os.environ.get("SECRET_KEY")
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
			connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
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
			listDataB =[]
			dic = dict()
			for i in range(len(jsonB)):
				dictCombin = dict(zip(title,jsonB[i]))
				listData.append(dictCombin)
				dic[title0[1]] = listData
				dic[title0[0]] = 1	
				allimages=dic['data'][i]['images']
				splitA=allimages.split("'")
				splitA=list(filter((", ").__ne__, splitA))
				if "" in splitA :
					splitA.remove("")
					splitA=list(filter(("").__ne__, splitA))
					listDataB.append(splitA)	
					dic['data'][i]['images']=listDataB[i]
			return(jsonify(dic))
			cursor.close()
			connection.close()
		pageQuery = int(request.args.get('page',0))
		if keywordQuery == None: 	
			if pageQuery  ==  0 :
				connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
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
				title2 = ["nextpage"]
				listData = []
				listDataB =[]
				listDataC = []
				dic = dict()
				for i in range(len(jsonB)):
						dictCombin = dict(zip(title,jsonB[i]))
						listData.append(dictCombin)
						dic[title0[1]] = listData
						dic[title0[0]] = 1
						allimages=dic['data'][i]['images']
						splitA=allimages.split("'")
						splitA=list(filter((", ").__ne__, splitA))
						if "" in splitA :
							splitA.remove("")
						splitA=list(filter(("").__ne__, splitA))
						listDataB.append(splitA)	
						dic['data'][i]['images']=listDataB[i]
				return(jsonify(dic))
				cursor.close()
				connection.close()
			elif pageQuery > 0:
				connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
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
					listDataB=[]
					dic0 = dict()
					for i in range(len(jsonD)):
						dictCombin0 = dict(zip(title,jsonD[i]))
						listData0.append(dictCombin0)
						dic0[title0[1]] = listData0
						allimages=dic0['data'][i]['images']
						splitA=allimages.split("'")
						splitA=list(filter((", ").__ne__, splitA))
						if "" in splitA :
							splitA.remove("")
						splitA=list(filter(("").__ne__, splitA))
						listDataB.append(splitA)	
						dic0['data'][i]['images']=listDataB[i]
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
			connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
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
				listDataB =[]
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
							allimages=dic['data'][i]['images']
							splitA=allimages.split("'")
							splitA=list(filter((", ").__ne__, splitA))
							if "" in splitA :
								splitA.remove("")
							splitA=list(filter(("").__ne__, splitA))
							listDataB.append(splitA)	
							dic['data'][i]['images']=listDataB[i]
							
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
							allimages=dic['data'][i]['images']
							splitA=allimages.split("'")
							splitA=list(filter((", ").__ne__, splitA))
							if "" in splitA :
								splitA.remove("")
							splitA=list(filter(("").__ne__, splitA))
							listDataB.append(splitA)	
							dic['data'][i]['images']=listDataB[i]
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
				listDataB = []
				dic = dict()
				for i in range(len(jsonB)):
					if  pageQuery < 1:
						dictCombin = dict(zip(title,jsonB[i]))
						listData.append(dictCombin)
						dic[title0[1]] = listData
						allimages=dic['data'][i]['images']
						splitA=allimages.split("'")
						splitA=list(filter((", ").__ne__, splitA))
						if "" in splitA :
							splitA.remove("")
						splitA=list(filter(("").__ne__, splitA))
						listDataB.append(splitA)	
						dic['data'][i]['images']=listDataB[i]
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
		connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
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
		title0 = ["data","nextpage"]
		if 0 < id <=  58 :
			listDataA= []
			listDataB=[]
			dic = dict()
			for i in range(len(jsonB)):
				dictCombin = dict(zip(title,jsonB[i]))
				listDataA.append(dictCombin)
				dic[title0[0]] = listDataA
				allimages=dic['data'][i]['images']
				splitA=allimages.split("'")
				splitA=list(filter((", ").__ne__, splitA))
				if "" in splitA :
					splitA.remove("")
				splitA=list(filter(("").__ne__, splitA))
				listDataB.append(splitA)	
				dic['data'][i]['images']=listDataB[i]
				strA=str(dic['data'][i])
				a=dic['data'][i]
				dic[title0[0]]=a
			return(jsonify(dic))
		elif id>58 or id==0 :
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

@app.route("/api/user",methods = ["POST","GET","PATCH","DELETE"])
def user():
	jsonData=request.json
	
	if request.method == 'POST':
		email=jsonData["email"]
		password=jsonData["password"]
		username=jsonData["username"]
		# connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
		connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
		cursor  =  connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		sqlInsert="INSERT INTO `user_data`(`name`,`email`,`password`) VALUES (%s,%s,%s)"
		bindData=(username,email,password,)
		sqlSelect="SELECT `email` FROM `user_data` WHERE `email`=%s"
		cursor.execute(sqlSelect,(email,))
		results=cursor.fetchall()
		if len(results)!=0:
			connection.close()
			mailError={"error": True,'"message"': "Email已經註冊帳戶"}
			return (jsonify(mailError))
		else:
			cursor.execute(sqlInsert,bindData)
			connection.commit()
			connection.close()
		# signupDone={"ok": "true"}
		return (jsonify({"ok":True}))
	elif request.method == 'PATCH':
		email=jsonData["email"]
		password=jsonData["password"]
		#connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
		connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
		cursor  =  connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		sqlSelect="SELECT `email` FROM `user_data` WHERE `email`=%s and `password`=%s"
		cursor.execute(sqlSelect,(email,password,))
		results=cursor.fetchone()
		if  results:
			connection.close()
			session["email"]=email
			session["password"]=password
			signInOK={"ok":True}
			return (jsonify(signInOK))
		else:
			connection.close()
			signError={"error": "true","message": "請重新輸入"}
			return (jsonify(signError))
	elif request.method == 'GET':
		emailSession=session["email"]
		passwordSession=session["password"]
		#connection  =  mysql.connector.connect(host = "localhost" ,port = "3306" ,user = "root" ,password = "password")
		connection  =  mysql.connector.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD)
		cursor  =  connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		sqlSelect="SELECT `id`,`name`,`email` FROM `user_data` WHERE `email`=%s and `password`=%s"
		cursor.execute(sqlSelect,(emailSession,passwordSession,))
		results=cursor.fetchone()
		if  results:
			id = results[0]
			name =results[1]
			email =results[2]
			data={"data":{"id": id,"name": name,"email": email}}
			connection.close()
			return (jsonify(data))
		else:
			nullData={"data":NULL}
			connection.close()
			return (jsonify(nullData))
		
	elif request.method == 'DELETE':
		session["email"]=None
		session["password"]=None
		signOut={"ok":True}
		connection.close()
		return (jsonify(signOut))
# app.debug = True
app.run(host='0.0.0.0',port=3000)