import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
bucket = 'harshak-storage'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HS3-FileMetadata')


def dynamodb_deleter(filename):
    file_location = f"s3://{bucket}/{filename}"
    
    try:
        Item={
                'file_name': filename
            }
        table.delete_item(Key=Item)
        
        return {
            "status": "success", 
            "message": f"Deleted {filename} from DynamoDB"
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
        s3.delete_object(Bucket=bucket, Key=filename)
        dynamodb_deleter(filename)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"message": f"File '{filename}' deleted successfully.", "filename": filename})
        }

    except ClientError as e:
        print(f"S3 ClientError: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f"Error deleting file: {str(e)}")
        }

        
    except Exception as e:
        print(f"General Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }



# old code, only deletes the code
# import boto3
# import json
# from botocore.exceptions import ClientError

# s3 = boto3.client('s3')
# bucket = 'harshak-storage'

# def lambda_handler(event, context):
#     headers = {
#         "Access-Control-Allow-Origin": "*",
#         "Access-Control-Allow-Headers": "Content-Type",
#         "Access-Control-Allow-Methods": "OPTIONS,POST"
#     }

#     try:
#         raw_body = event.get('body')
#         if not raw_body:
#              return {
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
#         s3.delete_object(Bucket=bucket, Key=filename)
        
#         return {
#             'statusCode': 200,
#             'headers': headers,
#             'body': json.dumps({"message": f"File '{filename}' deleted successfully.", "filename": filename})
#         }

#     except ClientError as e:
#         print(f"S3 ClientError: {e}")
#         return {
#             'statusCode': 500,
#             'headers': headers,
#             'body': json.dumps(f"Error deleting file: {str(e)}")
#         }

        
#     except Exception as e:
#         print(f"General Error: {e}")
#         return {
#             'statusCode': 500,
#             'headers': headers,
#             'body': json.dumps(f"Internal server error: {str(e)}")
#         }
