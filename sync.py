import boto3
import json
import os
import uuid 
AWS_ACCESS_KEY_ID = os.environ.get('AccessKeyId')
AWS_SECRET_ACCESS_KEY = os.environ.get('SecretAccessKey')

dynamodb = boto3.resource('dynamodb',aws_access_key_id = AWS_ACCESS_KEY_ID , aws_secret_access_key = AWS_SECRET_ACCESS_KEY , region_name  = 'ap-south-1')

jsonfile = os.getcwd() + '\\sample_sync_data.json'

def write_single_item():
	table = dynamodb.Table('Classes')
	table.put_item(
	Item={
	        'ClassName': 'X',
	        'SectionName': 'C',
	        'email': 'gokulsadanandam@gmail.com',
	        'Students': [
    			"Gokul",
				"Muri",
    			"Velu"
  			]
    	}
	)

def sync_data(json):
	for data in json:
		write_batch(data,json[data])

def write_batch(classname,json):
	table = dynamodb.Table(classname)
	with table.batch_writer() as batch:
		for items in range(len(json)):
			json[items]['email'] = 'gokulsadanandam@gmail.com'
			json[items]['id'] = str(uuid.uuid4())
			batch.put_item(
            Item= json[items]
	        )


if __name__ == "__main__":
	write_single_item()
	jsonfile = open (jsonfile , 'r')
	jsondata = json.loads(jsonfile.read())
	sync_data(jsondata)