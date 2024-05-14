from calra_lambda import *
import json
import os

@GET('/dogs')
@runtime('python3.11')
@name('LBD-DOGS-GET')
@memory_size(256)
def lambda_handler(event, context):
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello World from /dogs!'
        })
    }
    return response

@GET('/cats')
@environment('DB_NAME_CATS')
@description("This Lambda implements functionality for the CATS service")
@timeout(30)
@name('LBD-CATS-GET')
def cat_handler(event, context):
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': f"Hello from cats handler GET. There is a custom environment called DB_NAME_CATS of value.. {os.environ['DB_NAME_CATS']}"
        })
    }
    return response

