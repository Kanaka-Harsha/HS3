# This function extracts the entire file size from the db of file Size and sends it back UI.
import json
import boto3
from decimal import Decimal

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table('HS3-FileMetadata')

def lambda_handler(event, context):
    total=0
    scan_arr={}
    while True:
        response=table.scan(**scan_arr)
        for item in response.get('Items',[]):
            if 'file_size_MB' in item:
               total+=Decimal(item['file_size_MB'])
        if 'LastEvaluatedKey' in response:
            scan_arr['ExclusiveStartKey'] = response['LastEvaluatedKey']
        else:
            break
    return {
        "statusCode" : 200,
        "headers" : {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*"
        },
        "body" : json.dumps({
            "totalSum" : Decimal(total)
        })
    }
 