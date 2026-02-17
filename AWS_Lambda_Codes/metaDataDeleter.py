import json
import urllib.parse
import boto3

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'HS3-MetaData'

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        table = dynamodb.Table(TABLE_NAME)
        
        response = table.delete_item(
            Key={
                'filename': key
            }
        )
        
        print(f"Successfully deleted metadata for {key} from DynamoDB")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully deleted metadata for {key}")
        }

    except Exception as e:
        print(f"Error processing delete for object {key} from bucket {bucket}.")
        print(e)
        raise e
