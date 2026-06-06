import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def lambda_handler(event, context):
    method = event.get('httpMethod', 'GET')
    
    if method == 'POST':
        body = json.loads(event.get('body') or '{}')
        note_id = str(uuid.uuid4())
        table.put_item(Item={
            'noteId': note_id,
            'title': body.get('title', ''),
            'content': body.get('content', ''),
            'createdAt': datetime.utcnow().isoformat()
        })
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'noteId': note_id})
        }
    
    result = table.scan()
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result['Items'])
    }
