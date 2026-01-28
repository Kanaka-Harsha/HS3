import json
import boto3
from decimal import Decimal

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table('HS3-FileMetadata')

def lambda_handler(event, context):

    event_keys=event

    items=[]
    kwargs={}
    # we have to use "scan" only for small table sizes and when we are unknown of data size
    while True:
        response=table.scan(**kwargs)
        items.extend(response.get('Items', []))
         if 'LastEvaluatedKey' in response:
            kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        else:
            break

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type' : 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(items, default=decimal_converter)
    }

def decimal_converter(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
