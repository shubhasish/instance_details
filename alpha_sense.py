import boto3
import pandas
import csv
import os

aws_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_key = os.environ.get('AWS_KEY')

file = open('ri_details.csv','w+')
csv_writer = csv.writer(file,delimiter=',')

ec2 = boto3.client('ec2',aws_access_key_id=aws_key_id,aws_secret_access_key=aws_key,region_name="us-east-1")

environment_temporary_set = set()


instances = ec2.describe_instances()
reservations = instances['Reservations']
name= None
environment = None
reservation = "None"
csv_writer.writerow(['Environment','Name','State','Instance Type'])
for reservation in reservations:
    instanceDetails = reservation['Instances'][0]
    instancetype = instanceDetails['InstanceType']
    state = instanceDetails['State']['Name']
    tags = instanceDetails['Tags']
    for tag in tags:
        if tag['Key'] == "Name":
            name = tag['Value']
        elif tag['Key'] == "environment":
            environment = tag['Value']
    environment_temporary_set.add(environment)
    row = [environment,name,state,instancetype]
    #print row
#print environment_temporary_set
    csv_writer.writerow(row)
file.close()