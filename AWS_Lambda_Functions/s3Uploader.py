import json
import boto3
from botocore.exceptions import ClientError
import urllib.parse
from decimal import Decimal
import datetime

s3 = boto3.client('s3')
bucket_name = "harshak-storage"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HS3-FileMetadata')


def dynamodb_uploader(filename, content_type, file_size=0):
    file_type = content_type
    
    if content_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
        file_type = 'pptx'
    elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        file_type = 'docx'
    elif content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        file_type = 'xlsx'
    elif content_type.startswith('image/'):
        file_type = 'image'
    elif content_type.startswith('video/'):
        file_type = 'video'
    elif content_type.startswith('audio/'):
        file_type = 'audio'
    elif content_type.startswith('text/'):
        file_type = 'txt'
    elif content_type == 'application/pdf':
        file_type = 'pdf'
        
    file_location = f"s3://{bucket_name}/{filename}"
    
    try:
        size_decimal = Decimal(str(file_size))
    except:
        size_decimal = Decimal('0')

    try:
        table.put_item(
           Item={
                'file_name': filename, 
                'file_size_MB': size_decimal,
                'file_type': file_type,
                'file_location': file_location,
                'file_upload_time': datetime.datetime.now().isoformat()
            }
        )
        
        return {
            "status": "success", 
            "message": f"Logged {filename} to DynamoDB"
        }

    except Exception as e:
        print(f"DynamoDB Error: {e}")
        raise e


def lambda_handler(event, context):

    headers = {
        "Access-Control-Allow-Origin": "*",
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
        file_size = body.get('file_size', 0)
        
        try:
            dynamodb_uploader(filename, content_type, file_size)

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
        except Exception as e:
             print(f"DynamoDB/Internal Error: {e}")
             return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps(f"Internal Error: {str(e)}")
            }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                "message": "Presigned URL generated and metadata logged.",
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








#just upload code


# import json
# import boto3
# from botocore.exceptions import ClientError
# import urllib.parse
# from decimal import Decimal
# import datetime

# s3 = boto3.client('s3')
# bucket_name = "harshak-storage"

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('HS3-FileMetadata')


# def dynamodb_uploader(filename, content_type, file_size=0):
#     file_type = content_type
    
#     if content_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
#         file_type = 'pptx'
#     elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#         file_type = 'docx'
#     elif content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
#         file_type = 'xlsx'
#     elif content_type.startswith('image/'):
#         file_type = 'image'
#     elif content_type.startswith('video/'):
#         file_type = 'video'
#     elif content_type.startswith('audio/'):
#         file_type = 'audio'
#     elif content_type.startswith('text/'):
#         file_type = 'txt'
#     elif content_type == 'application/pdf':
#         file_type = 'pdf'
        
#     file_location = f"s3://{bucket_name}/{filename}"
    
#     try:
#         size_decimal = Decimal(str(file_size))
#     except:
#         size_decimal = Decimal('0')

#     try:
#         table.put_item(
#            Item={
#                 'file_name': filename, 
#                 'file_size_MB': size_decimal,
#                 'file_type': file_type,
#                 'file_location': file_location,
#                 'file_upload_time': datetime.datetime.now().isoformat()
#             }
#         )
        
#         return {
#             "status": "success", 
#             "message": f"Logged {filename} to DynamoDB"
#         }

#     except Exception as e:
#         print(f"DynamoDB Error: {e}")
#         raise e


# def lambda_handler(event, context):

#     headers = {
#         "Access-Control-Allow-Origin": "*",
#         "Access-Control-Allow-Headers": "Content-Type",
#         "Access-Control-Allow-Methods": "OPTIONS,POST"
#     }

#     try:
#         raw_body = event.get('body')
#         if not raw_body:
#             return {
#                 'statusCode': 400,
#                 'headers': headers,
#                 'body': json.dumps("Error: Request body is empty.")
#             }

#         body = json.loads(raw_body)
        
#         if 'filename' not in body:
#             return {
#                 'statusCode': 400,
#                 'headers': headers,
#                 'body': json.dumps("Error: Missing 'filename' in request body.")
#             }

#         filename = body['filename']
#         content_type = body.get('content_type', 'application/octet-stream')
#         file_size = body.get('file_size', 0)
        
#         try:
#             dynamodb_uploader(filename, content_type, file_size)

#             presigned_url = s3.generate_presigned_url(
#                 'put_object',
#                 Params={
#                     'Bucket': bucket_name,
#                     'Key': filename,
#                     'ContentType': content_type
#                 },
#                 ExpiresIn=3600
#             )
            
#         except ClientError as e:
#             print(f"Error generating presigned URL: {e}")
#             return {
#                 'statusCode': 500,
#                 'headers': headers,
#                 'body': json.dumps(f"S3 Error: {str(e)}")
#             }
#         except Exception as e:
#              print(f"DynamoDB/Internal Error: {e}")
#              return {
#                 'statusCode': 500,
#                 'headers': headers,
#                 'body': json.dumps(f"Internal Error: {str(e)}")
#             }

#         return {
#             'statusCode': 200,
#             'headers': headers,
#             'body': json.dumps({
#                 "message": "Presigned URL generated and metadata logged.",
#                 "upload_url": presigned_url,
#                 "filename": filename
#             })
#         }

#     except Exception as e:
#         print(f"Handler failed: {str(e)}")
#         return {
#             'statusCode': 500,
#             'headers': headers,
#             'body': json.dumps(f"Error processing request: {str(e)}")
#         }
