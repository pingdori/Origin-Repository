from flask import *
import json
import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
from collections import defaultdict
from flask_cors import CORS
from flask import session
from werkzeug.security import generate_password_hash,check_password_hash
import os
from config import Config 
import time
import requests as req

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
load_dotenv()
MYSQL_HOST = os.environ.get("mysql_host")
MYSQL_PORT = os.environ.get("mysql_port")
MYSQL_USER = os.environ.get("mysql_user")
MYSQL_PASSWORD = os.environ.get("mysql_password")
app.secret_key = "123456"
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
				connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
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
				connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
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
			connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
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
		connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
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
	try:	
		if request.method == 'POST':
			email=jsonData["email"]
			password=jsonData["password"]
			username=jsonData["username"]
			connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
			cursor  =  connection.cursor()
			cursor.execute("USE `taipei-attractions`")
			sqlInsert="INSERT INTO `user_data`(`name`,`email`,`password`) VALUES (%s,%s,%s)"
			bindData=(username,email,password,)
			sqlSelect="SELECT `email` FROM `user_data` WHERE `email`=%s"
			cursor.execute(sqlSelect,(email,))
			results=cursor.fetchall()
			if len(results)!=0:
				connection.close()
				mailError={"error": True,"message": "Email已經註冊帳戶"}
				return (jsonify(mailError))
			elif username == "" or email == "" or password=="":
				Error={"error": True,"message": "請輸入帳號或密碼"}
				return (jsonify(Error))
			else:
				cursor.execute(sqlInsert,bindData)
				connection.commit()
				connection.close()
			# signupDone={"ok": "true"}
			return (jsonify({"ok":True}))
		elif request.method == 'PATCH':
			email=jsonData["email"]
			password=jsonData["password"]
			connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
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
			if  session["password"]!=None:
				emailSession=session["email"]
				passwordSession=session["password"]
				connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
				cursor  =  connection.cursor()
				cursor.execute("USE `taipei-attractions`")
				sqlSelect="SELECT `id`,`name`,`email` FROM `user_data` WHERE `email`=%s and `password`=%s"
				cursor.execute(sqlSelect,(emailSession,passwordSession,))
				results=cursor.fetchone()
				id = results[0]
				name =results[1]
				email =results[2]
				data={"data":{"id": id,"name": name,"email": email}}
				connection.close()
				return (jsonify(data))
			elif session["password"] == None:
				nullData={"data":"null"}
				return (jsonify(nullData))
			
		elif request.method == 'DELETE':
			session["email"]=None
			session["password"]=None
			signOut={"ok":True}
			return (jsonify(signOut))
	except:
		nullData={"data":"null"}
		return (jsonify(nullData))
		
@app.route("/api/booking",methods = ["POST","GET","DELETE"])
def Booking():
	jsonData=request.json
	try:
		connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
		cursor  =  connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		signInOK={"ok":True}
		if request.method == 'POST':	
			attractionId=jsonData["attractionId"]
			session["attractionId"]=attractionId
			date=jsonData["date"]
			session["date"]=date
			time=jsonData["time"]
			session["time"]=time
			price=jsonData["price"]
			session["price"]=price
			print(price)
			sqlSelect="SELECT `mail` FROM `booking_data` WHERE `mail`=%s "
			sqlUpdate="Update `booking_data` SET `attractionId`=%s,`date`=%s,`time`=%s,`price`=%s WHERE `mail`=%s "
			sqlInsert="INSERT INTO `booking_data`(`attractionId`,`date`,`time`,`price`,`mail`) VALUES (%s,%s,%s,%s,%s)"
			mail=session["email"]
			if  session["password"]!=None:
				if date!="" or time != None or price!=None :
					cursor.execute(sqlSelect,(mail,))
					results=cursor.fetchone()
					if results:
						cursor.execute(sqlUpdate,(attractionId,date,time,price,mail,))
						connection.commit()
						connection.close()
						return(jsonify(signInOK))
					else:
						cursor.execute(sqlInsert,(attractionId,date,time,price,mail,))
						connection.commit()
						connection.close()
						return(jsonify(signInOK))
				elif date=="" or time == None or price==None:
					dataError={"error": "true","message": "建立失敗"}
					return(jsonify(dataError))
			elif session["password"] == None:
				passwordError={"error": "true","message": "未登入系統，拒絕存取"}
				return(jsonify(passwordError))
		if request.method == 'GET':
			if session["attractionId"]!=None:
				attractionId=session["attractionId"]
				date=session["date"]
				time=session["time"]
				price=session["price"]
				cursor.execute("SELECT `data`.`id`,`data`.`name`,`address`,`images` from `data`Join  `data_images` on `data`.`name` = `data_images`.`name` and `data`.`id` like %s ",(attractionId,))
				results=cursor.fetchone()
				jsonA = json.dumps(results)
				jsonB = json.loads(jsonA) 
				Id=jsonB[0]
				name=jsonB[1]
				address=jsonB[2]
				image=jsonB[3]
				imageSplit=image.split(",")
				imageSplit0=image.split("'")
				data={"data":{"attraction":{"id":attractionId,"name":name,"address":address,"image":imageSplit0[1]},"date":date,"time":time,"price":price}}
				session["data"]=data
				return(jsonify(data))
			else:
				dataError={"error": "true","message": "無預定行程"}
				return(jsonify(dataError))
			
		if request.method == 'DELETE':
			
			cursor.execute("DELETE FROM `booking_data` WHERE `mail` =%s",(session["email"],))
			session["attractionId"]=None
			connection.commit()
			connection.close()
			
			
			return(signInOK)
	except:
		dataError={"error": "true","message": "無預定行程"}
		return (jsonify(dataError))	

@app.route("/api/orders", methods=['GET', 'POST'])
def order():
	try:
		jsonData=request.json
		connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
		cursor  =  connection.cursor()
		cursor.execute("USE `taipei-attractions`")
		sqlUpdate="Update `New_order_data` SET `order_status`=%s WHERE `prime`=%s"
		sqlInsert="INSERT INTO `New_order_data` (`number`,`prime`,`price`,`data_id`,`name`,`address`,`image`,`date`,`time`,`contact_name`,`email`,`phone`,`order_status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		prime=jsonData["prime"]
		price=jsonData["order"]["price"]
		data_id=jsonData["order"]["trip"]["attraction"]["id"]
		name=jsonData["order"]["trip"]["attraction"]["name"]
		address=jsonData["order"]["trip"]["attraction"]["address"]
		image=jsonData["order"]["trip"]["attraction"]["image"]
		date=jsonData["order"]["trip"]["date"]
		tripTime=jsonData["order"]["trip"]["time"]
		contactName=jsonData["order"]["contact"]["name"]
		email=jsonData["order"]["contact"]["email"]
		phone=jsonData["order"]["contact"]["phone"]
		orderStatusNO= "未付款"
		orderStatusYes= "已付款"
		orderNum = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-5:])
		partner_key= "partner_7rJA5A1PtHVvR4F9f8cQtZ7yP9l8y50J6gXUzLnss1YmCrRMCprL1ycY"
		merchant_id = "dorisLee_CTBC"
		if request.method == "POST":
			
			cursor.execute(sqlInsert,(orderNum,prime,price,data_id,name,address,image,date,tripTime,contactName,email,phone,orderStatusNO,))
			connection.commit()
			cursor.execute("SELECT `prime`,`number` FROM `New_order_data` WHERE `prime`=%s",(prime,))
			results  =  cursor.fetchone()
			jsonA  =  json.dumps(results)
			jsonB = json.loads(jsonA) 
			print(jsonB)
			requestTappayData = {
						'URL': 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime',
						'headers': {
							'Content-Type': 'application/json',
							'x-api-key': partner_key				
						},
						'body': {
							"prime": jsonData["prime"],
							"partner_key": partner_key,
							"merchant_id": merchant_id,
							"amount": str(jsonData["order"]["price"]),
							"details":"TapPay Test",
							"cardholder": {
								"phone_number": jsonData["order"]['contact']['phone'],
								"name": jsonData["order"]['contact']['name'].encode("utf-8").decode("latin1"),
								"email": jsonData["order"]['contact']['email'],
								"zip_code": "",
								"address": "",
								"national_id": ""
							},
							"remember": True
						},
					}
			requestTappay = req.post(
						requestTappayData['URL'],
						headers = requestTappayData['headers'],
						data = json.dumps(requestTappayData['body'], ensure_ascii=False)
					)
			if requestTappay.status_code == 200:
				cursor.execute(sqlUpdate,(orderStatusYes,jsonB[0],))
				connection.commit()
				connection.close()
				orderOK={
					"data": {
						"number": jsonB[1],
						"payment": {
						"status": 0,
						"message": "付款成功"
						}
					}
					}
				print(orderOK)
			return (jsonify(orderOK))
	except:
		dataError={
				"error": "true",
				"message": jsonB[1]
				}
		return (jsonify(dataError))	
@app.route("/api/order/<orderNumber>", methods=['GET'])
def orderNumber(orderNumber):
	connection  =  mysql.connector.connect(host = "0.0.0.0" ,port = "3306" ,user = "root" ,password = "Password123...")
	cursor  =  connection.cursor()
	cursor.execute("USE `taipei-attractions`")
	sqlSelect="SELECT `number`,`price`,`data_id`,`name`,`address`,`image`,`date`,`time`,`contact_name`,`email`,`phone`,`order_status` FROM `New_order_data` WHERE `number`=%s "
	cursor.execute(sqlSelect,(orderNumber,))
	results  =  cursor.fetchone()
	jsonA  =  json.dumps(results)
	jsonB = json.loads(jsonA) 
	if jsonB[11]=="已付款":
		status=1
	else:
		status=0
	print(jsonB)
	orderOK={
			"data": {
				"number": jsonB[0],
				"price": jsonB[1],
				"trip": {
				"attraction": {
					"id": jsonB[2],
					"name": jsonB[3],
					"address": jsonB[4],
					"image": jsonB[5]
				},
				"date": jsonB[6],
				"time": jsonB[7]
				},
				"contact": {
				"name": jsonB[8],
				"email": jsonB[9],
				"phone": jsonB[10]
				},
				"status": status
			}
			}
	return (jsonify(orderOK))


app.debug = True
app.run(host='0.0.0.0',port=3000)