import json
import urllib.parse
import boto3
from datetime import datetime
import time

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'HS3-MetaData'

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        response = s3.head_object(Bucket=bucket, Key=key)
        size = response['ContentLength']
        content_type = response['ContentType']
        
        table = dynamodb.Table(TABLE_NAME)
        
        timestamp = int(time.time())
        upload_date = datetime.now().strftime('%Y-%m-%d')
        
        access_url = f"https://{bucket}.s3.amazonaws.com/{key}"
        
        item = {
            'filename': key,
            'bucket': bucket,
            'file_size': size,
            'content_type': content_type,
            'upload_date': upload_date,
            'upload_timestamp': timestamp,
            'access_url': access_url
        }
        
        table.put_item(Item=item)
        
        print(f"Successfully indexed {key} from {bucket} into DynamoDB")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully indexed {key}")
        }

    except Exception as e:
        print(f"Error processing object {key} from bucket {bucket}.")
        print(e)
        raise e
