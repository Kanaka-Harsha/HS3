import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
bucket_name = "harshak-storage"

def lambda_handler(event, context):

    headers = {
        "Access-Control-Allow-Origin": "*", # Adjust this to your domain for production
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }

    try:
        raw_body = event.get('body')
        if not raw_body:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps("Error: Request body is empty.")
            }

        body = json.loads(raw_body)
        
        if 'filename' not in body:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps("Error: Missing 'filename' in request body.")
            }

        filename = body['filename']
        content_type = body.get('content_type', 'application/octet-stream')
        
        try:
            presigned_url = s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': filename,
                    'ContentType': content_type
                },
                ExpiresIn=3600
            )
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps(f"S3 Error: {str(e)}")
            }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                "message": "Presigned URL generated successfully.",
                "upload_url": presigned_url,
                "filename": filename
            })
        }

    except Exception as e:
        print(f"Handler failed: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f"Error processing request: {str(e)}")
        }