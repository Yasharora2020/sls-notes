import json
import boto3
import os
import botocore
import uuid
from botocore.exceptions import ClientError



NOTES_TABLE_NAME = os.environ['NOTES_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(NOTES_TABLE_NAME)


def createNote(event, context):
    data = json.loads(event['body'])
    print (data)
    item = {
        'notesId': str(uuid.uuid4())      ,#data['notesId'],
        'title': data['title'],
        'body': data['body']
        
    }
    
    try:
        table.put_item(Item=item, ConditionExpression='attribute_not_exists(notesId)')
        response = {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            response = {
                'statusCode': 400,
                'body': json.dumps({'message': 'Item already exists'})
            }
        else:
            response = {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }
    return response




def updateNote(event, context):
    try:
        notes_id = event['pathParameters']['id']
        data = json.loads(event['body'])
        response = table.update_item(
            Key={'notesId': notes_id},
            UpdateExpression='set title = :title, body = :body',
            ExpressionAttributeValues={
                ':title': data['title'],
                ':body': data['body']
            },
            ConditionExpression='attribute_exists(notesId)',
            ReturnValues='UPDATED_NEW'
        )

        return {
            'statusCode': 200,
            'body': json.dumps(response['Attributes'])
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request'})
        }

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Note not found'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }

def deleteNote(event, context):
    try:
        notes_id = event['pathParameters']['id']
        table.delete_item(
            Key={'notesId': notes_id},
            ConditionExpression='attribute_exists(notesId)'
        )
        response = {
            'statusCode': 200,
            'body': json.dumps(notes_id)
        }
    except KeyError as e:
        response = {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request'})
        }
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            response = {
                'statusCode': 404,
                'body': json.dumps({'message': 'Note not found'})
            }
        else:
            response = {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }
    return response


def getAllNotes(event, context):
    try:
        params = {'TableName': NOTES_TABLE_NAME}
        notes = table.scan(**params)['Items']
        return {
            'statusCode': 200,
            'body': json.dumps(notes)
        }
    except botocore.exceptions.ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }



def getNoteById(event, context):
    print('Event:', event)
    try:
        notes_id = event['pathParameters']['id']
        print('notes_id:', notes_id)
        note = getNoteById(notes_id)
        print('note:', note)
        if note:
          response = {
            'statusCode': 200,
            'body': json.dumps(note)
        }
        else:
            response = {
            'statusCode': 404,
            'body': json.dumps({'message': 'Note not found'})
           }
    except KeyError as e:
        response = {
         'statusCode': 400,
         'body': json.dumps({'message': 'Bad request'})
        }
    except botocore.exceptions.ClientError as e:
     response = {
         'statusCode': 500,
         'body': json.dumps({'message': str(e)})
     }
    return response



