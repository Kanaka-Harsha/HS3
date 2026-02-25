import json
import boto3
import uuid
from decimal import Decimal

# Custom encoder to handle DynamoDB Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bucket_name = 'hs3-storage' 
TABLE_NAME = 'HS3-MetaData'

def lambda_handler(event, context):
    http_method = event.get('httpMethod')

    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('CORS Preflight JSON')
        }

    if http_method == 'GET':
        try:
            table = dynamodb.Table(TABLE_NAME)
            response = table.scan()
            items = response.get('Items', [])
            
            # Generate pre-signed URLs for downloading each file
            for item in items:
                try:
                    signed_url = s3_client.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': bucket_name,
                            'Key': item['filename']
                        },
                        ExpiresIn=3600 # URL valid for 1 hour
                    )
                    item['access_url'] = signed_url
                except Exception as url_error:
                    print(f"Error signing URL for {item['filename']}: {str(url_error)}")
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(items, cls=DecimalEncoder)
            }
        except Exception as e:
            print(f"Error fetching metadata: {str(e)}")
            return {
                'statusCode': 500,
                'headers': { 'Access-Control-Allow-Origin': '*' },
                'body': json.dumps(f"Internal Server Error: {str(e)}")
            }

    if http_method == 'POST':
        try:
            body = json.loads(event['body'])
            filename = body.get('filename')
            content_type = body.get('content_type')
            
            if not filename or not content_type:
                return {
                    'statusCode': 400,
                    'headers': { 'Access-Control-Allow-Origin': '*' },
                    'body': json.dumps('Missing filename or content_type')
                }

            key = f"uploads/{uuid.uuid4()}-{filename}"

            upload_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': key,
                    'ContentType': content_type
                },
                ExpiresIn=3600 
            )

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({
                    'upload_url': upload_url,
                    'filename': key
                }, cls=DecimalEncoder)
            }

        except Exception as e:
            print(f"Error generating pre-signed URL: {str(e)}")
            return {
                'statusCode': 500,
                'headers': { 'Access-Control-Allow-Origin': '*' },
                'body': json.dumps(f"Internal Server Error: {str(e)}")
            }

    return {
        'statusCode': 405,
        'headers': { 'Access-Control-Allow-Origin': '*' },
        'body': json.dumps(f"Method {http_method} not allowed")
    }
