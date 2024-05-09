from calra_lambda import *
import json

@GET('/dogs')
@runtime('python3.11')
@environment('DB_NAME_DOGS')
@memory_size(256)
def dog_handler(event, context):
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from dogs handler GET'
        })
    }
    return response

@GET('/cats')
@environment('DB_NAME_CATS')
@description("This Lambda uses an alternative DB URL and PORT")
@timeout(30)
def cat_handler(event, context):
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from cats handler GET'
        })
    }
    return response

