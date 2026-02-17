import json
import boto3
import uuid

s3_client = boto3.client('s3')
bucket_name = 'hs3-storage' 

def lambda_handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return 
        {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps('CORS Preflight JSON')
        }

    try:
        body = json.loads(event['body'])
        filename = body.get('filename')
        content_type = body.get('content_type')
        
        if not filename or not content_type:
            return 
            {
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
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'upload_url': upload_url,
                'filename': key
            })
        }

    except Exception as e:
        print(f"Error generating pre-signed URL: {str(e)}")
        return 
        {
            'statusCode': 500,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps(f"Internal Server Error: {str(e)}")
        }
