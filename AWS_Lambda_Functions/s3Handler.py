# This lambda will get called whenever a file is uploaded into s3, and send the file details into the db
import boto3
import urllib.parse
from decimal import Decimal


s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HS3-FileMetadata')

def lambda_handler(event, context):
    #Get the bucket name and file name (key) from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    

    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        
        file_size = Decimal(str(round(response['ContentLength'] / (1024 * 1024),2)))
        file_type = response['ContentType']
        file_location = f"s3://{bucket}/{key}"

        if file_type=='application/vnd.openxmlformats-officedocument.presentationml.presentation':
            file_type='pptx'
        elif file_type=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            file_type='docx'
        elif file_type=='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            file_type='xlsx'
        elif file_type.startswith('image/'):
            file_type='image'
        elif file_type.startswith('video/'):
            file_type='video'
        elif file_type.startswith('audio/'):
            file_type='audio'
        elif file_type.startswith('text/'):
            file_type='txt'
        elif file_type == 'application/pdf':
            file_type = 'pdf'

        

        table.put_item(
           Item={
                'file_name': key.split('/')[-1], 
                'file_size_MB': file_size,
                'file_type': file_type,
                'file_location': file_location,
                'file_upload_time': response['LastModified'].isoformat()
            }
        )
        
        return 
        {
            "status": "success", 
            "message": f"Logged {key} to DynamoDB"
        }

    except Exception as e:
        print(f"Error: {e}")
        raise e