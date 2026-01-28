import json
import boto3

s3=boto3.client('s3')
bucket_name="harshak-storage"

def lambda_handler(event,context):
    