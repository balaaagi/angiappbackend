#!flask/bin/python
from flask import Flask,jsonify,request
from time import sleep
import requests
import urllib2
import json
import settings
import kairos_face
import urlparse
import re

kairos_face.settings.app_id = settings.app_id
kairos_face.settings.app_key = settings.app_key

app = Flask(__name__)

def verifyFunctionForMobile(img_url):
	mobileApiResponse={}
	try:
		recognized_faces = kairos_face.recognize_face(url=img_url, gallery_name=settings.gallery_name)
		r_faces=jsonify(recognized_faces)
		successCount=0
		successImage={}
		validateParams={}
		for image in recognized_faces['images']:
			if(successCount>1):
				break
			else:
				if(image['transaction']['status']=='success'):
					successCount=successCount+1
					successImage=image
		if(successCount==0):
			mobileApiResponse['status']='failure'
			mobileApiResponse['errmessage']="No Image Found"
			return jsonify(mobileApiResponse)
		elif(successCount==1):
			mobileApiResponse['status']='success'
			return jsonify(mobileApiResponse)
		else:
			mobileApiResponse['status']='failure'
			mobileApiResponse['errmessage']="Found Many Images"
			return jsonify(mobileApiResponse)
	except Exception as e:
		# print "okok",e
		# m = re.match(r"(\"Errors\")", str(e))
		# print m.group(1)
		# eAsJson=json.loads(str(e))
		# eAsJson=jsonify(str(e))
		# print eAsJson
		# print eAsJson.text
		# if(eAsJson['Errors']>5000):
		# 	# To DO Invoke OpenCV Functions
		print "Failure To Check for ",img_url
		mobileApiResponse['status']='failure'
		mobileApiResponse['errmessage']="Image Not Good"
		return jsonify(mobileApiResponse)

def verifyFunction(img_url,img_id):
	validateurl="https://us-central1-lynkhacksmock.cloudfunctions.net/verifyface"
	mobileApiResponse={}
	try:
		recognized_faces = kairos_face.recognize_face(url=img_url, gallery_name=settings.gallery_name)
		r_faces=jsonify(recognized_faces)
		print r_faces
		successCount=0
		successImage={}
		validateParams={}
		for image in recognized_faces['images']:
			if(successCount>1):
				break
			else:
				if(image['transaction']['status']=='success'):
					successCount=successCount+1
					successImage=image
		if(successCount==0):
			mobileApiResponse['status']='failure'
			mobileApiResponse['errmessage']="No Image Found"
			return jsonify(mobileApiResponse)
		elif(successCount==1):
			mobileApiResponse['status']='success'
			idname=successImage['candidates'][0]['subject_id']
			print idname
			validateParams['teamname']="illicitdevs"
			validateParams['imageuid']=img_id
			validateParams['name']=idname
			response = requests.post(validateurl, data={'teamname':'illicitdevs','imageuid':img_id,'name':idname})
			print response.content
			return jsonify(mobileApiResponse)
		else:
			mobileApiResponse['status']='failure'
			mobileApiResponse['errmessage']="Found Many Images"
			return jsonify(mobileApiResponse)
	except Exception as e:
		# print "okok",e
		# m = re.match(r"(\"Errors\")", str(e))
		# print m.group(1)
		# eAsJson=json.loads(str(e))
		# eAsJson=jsonify(str(e))
		# print eAsJson
		# print eAsJson.text
		# if(eAsJson['Errors']>5000):
		# 	# To DO Invoke OpenCV Functions
		print "Failure To Check for ",img_url,img_id
		response = requests.post(validateurl, data={'teamname':'illicitdevs','imageuid':img_id,'name':'notfound'})
		print response.content
		return jsonify(mobileApiResponse)



@app.route('/')
def index():
    print settings.TRAINING_URL
    return "Hello, World!"

@app.route('/verifyalltrainingset',methods=['GET'])
def train():
	response=requests.get(settings.TRAINING_URL)
	print response
	# return jsonify(json.loads(response.content))
	training_images=json.loads(response.content)
	count=1;
	for training_image in training_images:
		if(count%25==0):
			# break
			sleep(65)
		verifyFunction(training_image['url'],training_image['imageuid'])	
		# verifyResponse=requests.get('http://localhost:8576/verify?url='+training_image['url']+'&imageuid='+training_image['imageuid'])
		# print verifyResponse	
		print training_image['url'],training_image['imageuid']
		count=count+1
	return "Completed"

@app.route('/verify',methods=['GET'])
def verify():
	validateurl="https://us-central1-lynkhacksmock.cloudfunctions.net/verifyface"
	url=request.args.get('url')
	image_id=request.args.get('imageuid')
	token=request.args.get('token')
	imageUrlToVerify=url
	return verifyFunction(url,image_id)


@app.route('/verifyfrommobile',methods=['GET'])
def verifyformobile():
	url=request.args.get('url')
	token=request.args.get('token')
	imageUrlToVerify=url
	return verifyFunctionForMobile(url)


if __name__ == '__main__':
	app.run(port=8576,debug=True)


