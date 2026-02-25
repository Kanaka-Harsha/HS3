import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user-logins')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        input_username = body['username']
        input_password = body['password']
        
        response = table.get_item(
            Key={
                'username': input_username
            }
        )
        if 'Item' in response:
            user_data = response['Item']
            if user_data['password'] == input_password:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Login Success! Welcome back.'})
                }
            else:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'message': 'Invalid Password.'})
                }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User does not exist.'})
            }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error'})
        }