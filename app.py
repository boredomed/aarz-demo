#!/usr/bin/env python
import math
import urllib
from collections import OrderedDict
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
from flask import Flask
from flask import request
from flask import make_response
import psycopg2
x=os.environ['DATABASE_URL'] = "postgres://solrwgieezdudx:9a9654815c43e749fb35630a403d60b6a30c33691ec4b5f96ad320e4e65dd002@ec2-107-20-250-195.compute-1.amazonaws.com:5432/d9m3jramvhf5pq"
urllib.parse.uses_netloc.append("postgres")
db_url = urllib.parse.urlparse(os.environ['DATABASE_URL']) 
conn = psycopg2.connect(
    database=db_url.path[1:],
    user=db_url.username,
    password=db_url.password,
    host=db_url.hostname,
    port=db_url.port
)
users_info={}
#user_info.update({'a':{0,1}})
cursor=conn.cursor()
# Flask app should start in global layout
app = Flask(__name__)
intent_name="string"
@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	print("Request:")
	print(json.dumps(req, indent=4))
	res = processRequest(req)
	res = json.dumps(res, indent=4)
	print("after json.dumps",res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def processRequest(req):
	if req.get("result").get("action") != "final_budget":
		return {}
	global city_names
	global QR
	global intent_name
	global s_id
	global str
	global r_slug
	global im_url
	intent_name=processIntentName(req)
	city_names=processlocation(req)
	property_type=processPropertyType(req)
	maximum_valu=processMaximum(req)
	price_unit=processPriceUnit(req)
	max_area=processAreaMax(req)
	unit_property=processUnits(req)
	s_id=processsession(req)
	maximum_value=convertMaximum(maximum_valu, price_unit)
	print(maximum_value)
	print("this is session id:",s_id)
	#baseurl = "https://aarz.pk/bot/index.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
	#baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&price_min="+maximum_value+"&price_max=0estate_agent=&purpose=Sell&property_type="+property_type
	if maximum_value == 0:
		baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&type="+property_type+"&land_area="+unit_property+"&min_r=0&max_r="+max_area
	else:  
		baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&type="+property_type+"&price_max="+maximum_value+"&land_area="+unit_property+"&min_r=0&max_r="+max_area
	#print("city:",city_names)
	print("url is:",baseurl)
	result = urllib.request.urlopen(baseurl).read()
	#print('result of url:', result)
	data = json.loads(result)
	#print('data:', data)
	#res2=json_to_text(data)
	res2 = makeWebhookResult(data)
	print('res2:',res2)
	return res2

def processIntentName(req):
	result = req.get("result")
	parameters = result.get("metadata")
	intent = parameters.get("intentName")
	return intent
def processsession(req):
	session_id = req.get("sessionId")
	#print(session_Id)
	return session_id
def recommendationalgo(**user_info):
	rating=10

	buy1={}

	buy2={}

	smallbuy={}


	avgmid={}

	avg=0

	avrg={}

	hcount=0

	actualvector={}


	mod1=0
	mod2=0
	modict1={}
	modict2={}

	vecmul=0
	reslt=0

	simdict={s_id:{}}
	suggestiondic={}
	simusrs={}
	simusr=[]
	s_list=[]

	sstr='no recommendation yet'
	hfh='no recommendation yet'
	housecount=0
	hcountf=0
	housekey=''
	cityy=''
	fcnt=0
	
	#row_title=['1500 Square Feet C Type Apartment for Sale in i-11 karachi','C type apartment for sale in i-11 karachi']
	cominglist={}
	comingdata={}
	buy1={}
	
	print ("this is user info:", user_info)
	#d={'0db85c4d-2f65-403d-a67e-e8af469ee685': {'1 Kanal Plot For Sale In DHA Phase-8', '1 Kanal West Open Corner Brand New Bungalow Is Available For Sale', '26.64 Marla House For Rent ', '900 Square Feet Apartment for Sale in Karachi Rahat Commercial Area'}, 'ab8f9722-1925-49cd-ab28-05aad09ddc3e': {'5 Marla Residential Land for Sale in Karachi Bahria Town', '4.4 Marla Residential Land for Sale in Karachi Bahria Town'}, '40efe1a9-f019-4328-b86e-cf14c4eac4ef': {'1 Kanal Bungalow Available For Sale in AFOHS New Malir', '1 Kanal Plot For Sale In DHA Phase-8', '26.64 Marla House For Rent ', '1 Kanal West Open Corner Brand New Bungalow Is Available For Sale'}}
	rating=10
	ndlist={}
	for key in user_info:
		for house in user_info[key]:
			ndlist.update({house:rating})
			rating=rating-2
		rating=10
		buy1.update({key:ndlist})
		ndlist={}

	print ("this is buy1:",buy1)

	#buy1={'1C1':{'1450 Square Feet Apartment for Sale in karachi F-10':10,'666 Square Yard Plot for Sale in karachi F-10/2':8,'C type apartment for sale in i-11 karachi':4},
	#'1C2':{'1 Kanal Residential Land for Sale in karachi DHA Defence':10,'15 Marla House for Sale in karachi Abshar Colony':8},
	#'1C3':{'10.6 Marla House for Sale in karachi Double Road':10,'5 Marla House for Sale in karachi Chilten Housing Scheme':8},
	#'1C4':{'1 Kanal House for Sale in karachi Bahria Town':10,'10 Marla House for Sale in karachi Bahria Town Phase-2':8},
	#'1C5':{'1 Kanal Bungalow Available For Sale in AFOHS New Malir':10,'1 Kanal Plot For Sale In DHA Phase-8 karachi':8},
	#'1C6':{'1 Kanal House For Sale In Askari-5, karachi':10,'1 Kanal House for Rent in karachi DHA Phase-5 Block K':8}}





	#storage

	for val in row_title:
		cominglist.update({val:rating})
		rating=rating-2
	comingdata.update({s_id:cominglist})

	if s_id not in buy1:
		buy1.update(comingdata)
	else:
		buy1[s_id].update(cominglist)


	#print (buy1)




	#taking average

	for outerkey in buy1:
		avgmid.update(buy1[outerkey])
		for key in avgmid:
			avg=avg+avgmid[key]
			hcount=hcount+1
		avrg.update({outerkey:avg/hcount})
		avg=0
		avgmid.clear()
		hcount=0




	#centered cosine

	for outerkey in buy1:
		buy2.update({outerkey:buy1[outerkey]})
		for okey in buy2:
			smallbuy.update(buy2[okey])
			for key in smallbuy:
				smallbuy[key]=smallbuy[key]-avrg[outerkey]
			actualvector.update({outerkey:smallbuy})
			smallbuy={}
		buy2.clear()
	
	#print ("Actual vector:",actualvector)





	#cosine similarity

	for house in comingdata:
		modict1.update(comingdata[house])
	#print ("modict1:",modict1)
	for value in modict1:
			mod1=mod1+(modict1[value]*modict1[value])
	mod1=math.sqrt(mod1)
	#print ("mod1:",mod1)

	for key in buy1:
		if (key!=s_id):
			modict2.update(buy1[key])
			if(key=='1C2'):
				print ("modict2:",modict2)
			for value in modict2:
				mod2=mod2+(modict2[value]*modict2[value])
			mod2=math.sqrt(mod2)
			if(key=='1C2'):
				print ("mod2:",mod2)
			for value in modict1:
				#print ("value of modict1 to be checked:",value)
				if value in modict2:
					vecmul=vecmul+(modict1[value]*modict2[value])
					if (key=='1C2'):
						print ("vector multiplication:", vecmul)	
			if(vecmul/(mod1*mod2)>0 and modict1!=modict2):
				simusr.append(key)
				if(key=='1C2'):
					print (vecmul/(mod1*mod2))				
			vecmul=0
			modict2={}
			mod2=0
	simusr.reverse()
	simdict.update({s_id:simusr})
	print (simdict)





	#suggesting

	for key in simdict[s_id]:
		for key2 in buy1[key]:
			if key2 not in buy1[s_id]:
				s_list.append(key2)		
	suggestiondic.update({s_id:s_list})

	print ("suggestion dictionary:",suggestiondic)


	shouslist=[]

	if (bool(suggestiondic[s_id])):
		#for house in suggestiondic.values():	
			#sstr=house[0]
		for hous in suggestiondic[s_id]:
			if city_names.lower() in hous.lower():
				shouslist.append(hous)
		print (shouslist)
		if len(shouslist) !=0:
			sstr=shouslist[0]


	#users who have no similar users


	if (not(bool(suggestiondic[s_id]))):
		for user in buy1:
			for house in buy1[user]:
				for user2 in buy1:
					if house in  buy1[user2]:
						housecount=housecount+1		
				if(housecount>hcountf):
					if (house not in buy1[s_id] and city_names.lower() in house.lower()):
						hcountf=housecount
						hfh=house
						#print ("andr agya house me kljkjdsljf:", hfh)
					housecount=0

		suggestiondic[s_id]=hfh
		sstr=hfh
	#print (suggestiondic)
	print ("suggested house:",sstr)
	
	return (sstr)
	
def processlocation(req):
	global city
	result = req.get("result")
	parameters = result.get("parameters")
	cityNames = parameters.get("location")
	city = cityNames.get("city")
	#print("city data:", city)
	#print("city:", city)

	return city

#Price and Unit
def processMaximum(req):
	result = req.get("result")
	parameters = result.get("parameters")
	act_pri = parameters.get("actual_price")
	if act_pri == '0':
		return act_pri
	else:
		maximum = act_pri.get("number")
	return maximum

def processPriceUnit(req):
	result = req.get("result")
	parameters = result.get("parameters")
	price_unit = parameters.get("price_unit")
	return price_unit

def processMinimum(req):
	result = req.get("result")
	parameters = result.get("parameters")
	min_price = parameters.get("min_price")
	return min_price

def processPropertyType(req):
	result = req.get("result")
	parameters = result.get("parameters")
	propertyType = parameters.get("PropertyType")
	return propertyType

def processAreaMax(req):
	result = req.get("result")
	parameters = result.get("parameters")
	max_area = parameters.get("max_area")
	return max_area

def processUnits(req):
	result = req.get("result")
	parameters = result.get("parameters")
	units = parameters.get("Unit")
	print(units)
	return units

def processProjectName(req):
	result = req.get("result")
	parameters = result.get("parameters")
	project_name = parameters.get("ProjectName")
	return project_name 

#Price
def convertMaximum(pric, unit):
	print(pric)
	price = int(pric)
	print(price)
	if unit[0] == 'z':
		price = int(pric)
	elif unit[0] == 'l' or unit[0] == 'L':
		price = price * (10 ** 5)
	elif unit[0] == 'm' or unit[0] == 'M':
		price = price * (10 ** 6)
	elif unit[0] == 'c' or unit[0] == 'C':
		price = price * (10 ** 7)
	print(price)
	return str(price)

def makeWebhookResult(data):
	i=0
	global row_title
	length=len(data)
	speech_data = "Here are some properties with your choice. We have total of "+str(length)+" records of your interest in city  "+city+"."
	text_data = "Here are some properties with your choice. We have total of "+str(length)+" records of your interest in city  "+city+"."
	recom_prop=['','',"No Recommendation Available",'','','','','']
	row_id=[1,2,3,4,5]
	row_title=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_location=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_price=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_slug=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_number=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_image=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_city=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	while (i <length):
		row_id[i]=data[i]['property_id']
		row_title[i]=data[i]['title']
		row_location[i]=data[i]['address']
		if row_location[i] == "" or row_location[i] == " ":
		   row_location[i] = "not specified"
		row_price[i]=data[i]['price']
		row_slug[i]=data[i]['slug']
		row_number[i]=data[i]['number']
		row_image[i]=data[i]['image']
		row_city[i]=data[i]['city_name']
		#sql code
		if "Unable" in row_title[0]: #if there is no data
			break  #don't run sql commands
		SQLCommand=("SELECT * FROM Property WHERE Property.prop_id=%d"%  (row_id[i])) #check if this property is already present in database
		print("PROPERTY ID1")
		print(row_id[i])
		Values=[8]
		cursor.execute(SQLCommand,Values)
		prop_check=cursor.fetchone() 
		if prop_check==None:#if 0 rows are returned insert that property in Property table
			print("ADDING NEW PROPERTY")
			SQLCommand1= ("INSERT INTO property(prop_id,city,title,address,number,slug,price,image) VALUES (%d,'%s','%s','%s','%s','%s',%d,'%s')" %(row_id[i],row_city[i],row_title[i],row_location[i],row_number[i],row_slug[i],row_price[i],row_image[i]))
			Values1=[8]
			cursor.execute(SQLCommand1,Values1);
		conn.commit()
		speech_data_parts="Here is record " + str(i+1) +":"+ row_title[i]+" in city "+row_city[i] + " price is "+ str(row_price[i]) + "."
		speech_data = speech_data + speech_data_parts
		text_data_parts ="Here is record " + str(i+1) +":"+ row_title[i]+" in city "+row_city[i] + " price is "+ str(row_price[i])+ ". For Info about this contact at number "+str(row_number[i]) + "."
		text_data = text_data + text_data_parts	
		i+=1
	print("CITY IS")	
	print(row_city[0])
	SQLCommand3 = ("SELECT u.sess_id,p.title FROM users u join property p on u.prop_id=p.prop_id WHERE p.city='%s' ORDER BY u.sess_id"%(city_names)) #select the all properties of this city searched by users
	Values3=[2]
	cursor.execute(SQLCommand3,Values3);
	userdata=cursor.fetchone()
	users_info={}
	if userdata!=None:
		print("USER DATA DICTIONARY")
		print(userdata)
		print("USER DATA END")
		while userdata:#to cater all the rows from the result
			if userdata[0] in users_info: #if that user is already in the dictionary, append to the houses list
				users_info[userdata[0]].update({userdata[1]})
			else: #if this user is not in the dictionary, add the data
				users_info.update({userdata[0]: {userdata[1]}})
			userdata=cursor.fetchone()
		print("USER INFO DICTIONARY")
		print(users_info)
		print("USER INFO END")
		print(row_title[0])
		algostr=recommendationalgo(**users_info)
		algos = "Recommeded for you: " + algostr
		#recommended property
		print(algos)
		SQLCommand4=("SELECT * FROM Property WHERE title='%s'"%(algostr))
		Values4=[8]
		cursor.execute(SQLCommand4,Values4);
		recom_prop=cursor.fetchone()
		print("recom_prop")
		print(recom_prop)
		text_data = text_data + algos
	j=0;
	while (j<length):
		if "Unable" in row_title[0]:
			break
		SQLCommand5=("SELECT * FROM Users WHERE Users.prop_id=%d and Users.sess_id='%s'"%(row_id[j],s_id)) #check if this user has already searched for this property
		Values5=[3]
		cursor.execute(SQLCommand5,Values5)
		user_check=cursor.fetchone()
		if user_check==None: #if this is the first time he searches for this property, add this info in Users table
			print("ADDING NEW USER")
			SQLCommand2=("INSERT INTO Users(sess_id,city,prop_id)VALUES ('%s','%s',%d)"%(s_id,row_city[j],row_id[j]))
			Values2=[3]
			cursor.execute(SQLCommand2,Values2);
		conn.commit()
		j+=1
	variable1=str(row_number[0])
	variable2=str(row_number[1])
	variable3=str(row_number[2])
	variable4=str(row_number[3]) 
	#print('speech Data',speech_data)
	#print('Text Data',text_data)
	if not recom_prop:
		if length==1:
			message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [{
               "title": row_title[0],
                "subtitle":row_location[0],
              "subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [
			{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable2[1:]
            },
                    {
                "type":"element_share"
                    
                    }
                   ]
          }, 
                {
             "title":"Recommended for you:"+"No recommendation available",
              "subtitle":"",
              "subtitle":"",
                "item_url":"",               
               "image_url":"" ,
             "buttons":[{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":""
                },
                 {
                "type":"element_share"
                  }
            ]
          }]
            
        }
      }
    }
		else:
			message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [
                   {
               "title": row_title[0],
                "subtitle":row_location[0],
              "subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable1[1:]
                },
                    {
                "type":"element_share"
                  
            }, 
                   ],
          }, 
                   {
               "title": row_title[1],
               "subtitle":row_location[1],
              "subtitle":"Price: Rs."+str(row_price[1]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[1],               
               "image_url":"https://www.aarz.pk/"+row_image[1]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable2[1:]
            }, 
                     {
                "type":"element_share"
                    
                    }, 
                   ],
          }, 
                  {
             "title":"Recommended for you:"+"No recommendation available",
              "subtitle":"",
              "subtitle":"",
                "item_url":"",               
               "image_url":"",
             "buttons":[{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":""
                },
                 {
                "type":"element_share"
                  }
            ]
          }
               ]
            }
         }
			}	
	elif "Unable" in row_title[0]:
		message={
	  "attachment":{
	   "type":"template",
	      "payload":{
	"template_type":"generic",
	"elements":[
          {
             "title":"Recommended for you:"+recom_prop[2],
              "subtitle":recom_prop[3],
              "subtitle":"Price: Rs."+str(recom_prop[6]),
                "item_url": "https://www.aarz.pk/property-detail/"+recom_prop[5],               
               "image_url":"https://www.aarz.pk/"+recom_prop[7] ,
             "buttons":[{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+recom_prop[4][1:]
                },
                 {
                "type":"element_share"
                  }
            ]
          }
        ]
      }
    }
  }
	elif length==1:
		message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [{
               "title": row_title[0],
                "subtitle":row_location[0],
              "subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [
			{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable2[1:]
            },
                    {
                "type":"element_share"
                    
                    }
                   ]
          }, 
                {
             "title":"Recommended for you:"+recom_prop[2],
              "subtitle":recom_prop[3],
              "subtitle":"Price: Rs."+str(recom_prop[6]),
                "item_url": "https://www.aarz.pk/property-detail/"+recom_prop[5],               
               "image_url":"https://www.aarz.pk/"+recom_prop[7] ,
             "buttons":[{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+recom_prop[4][1:]
                },
                 {
                "type":"element_share"
                  }
            ]
          }]
            
        }
      }
    }
	else:
		message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [
                   {
               "title": row_title[0],
                "subtitle":row_location[0],
              "subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable1[1:]
                },
                    {
                "type":"element_share"
                  
            }, 
                   ],
          }, 
                   {
               "title": row_title[1],
               "subtitle":row_location[1],
              "subtitle":"Price: Rs."+str(row_price[1]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[1],               
               "image_url":"https://www.aarz.pk/"+row_image[1]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable2[1:]
            }, 
                     {
                "type":"element_share"
                    
                    }, 
                   ],
          }, 
                  {
             "title":"Recommended for you:"+recom_prop[2],
              "subtitle":recom_prop[3],
              "subtitle":"Price: Rs."+str(recom_prop[6]),
                "item_url": "https://www.aarz.pk/property-detail/"+recom_prop[5],               
               "image_url":"https://www.aarz.pk/"+recom_prop[7] ,
             "buttons":[{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+recom_prop[4][1:]
                },
                 {
                "type":"element_share"
                  }
            ]
          }
               ]
            }
         }
}
	return {
        "speech": text_data,
        "displayText": text_data,
        "data": {"facebook": message},
        "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

app.run(debug=True, port=port, host='0.0.0.0')
conn.close()
