import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
bucket_name = "harshak-storage"

def lambda_handler(event, context):
    """
    generates an S3 Presigned URL for uploading files.
    expected event body: JSON string with 'filename' and optional 'content_type'.
    """
    try:
        body = json.loads(event['body'])
        
        if 'filename' not in body:
            return {
                'statusCode': 400,
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
            raise e

        return {
            'statusCode': 200,
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
            'body': json.dumps(f"Error processing request: {str(e)}")
        }
