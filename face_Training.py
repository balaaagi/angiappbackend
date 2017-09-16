
# Face deduction Image training based on JSON content from URL

import requests;
import json;
import sys;
import kairos_face;
impoty settings

kairos_face.settings.app_id = settings.app_id
kairos_face.settings.app_key = settings.app_key

image_url=settings.TRAINING_URL;

def call_image_train_method(img_url, p_name, img_id):
#	print img_url, p_name, img_id
	try:
		response=kairos_face.enroll_face(url=img_url, subject_id=p_name, gallery_name='AngiSample')
		if 'Errors' in response:
			print p_name+" Not loaded with the id="+ img_id+"\n";
		else:
			status=response['images'][0]['transaction']['status'];
			if(status=='success'):
				print p_name+" loaded successfully with the id="+ img_id+"\n";
			else:
				print p_name+" Not loaded with the id="+ img_id+"\n";
#	except ServiceRequestError:
	
	except:
		print p_name+" Not loaded with the id="+ img_id+"\n";
		
get_response = requests.get(url=image_url);

api_image_details=json.loads(get_response.content);

for i in api_image_details:
	try:
		url="";
		name="";
		imageuid="";
		if i['url'] != "":
			url=i['url'];
			if i['name'] != "":
				name=i['name']
			if i['imageuid'] != "":
				imageuid=i['imageuid']
			call_image_train_method(url, name,imageuid);
#			print url, name,imageuid;
#		break
	except NameError:
		print "No entry from image API";

