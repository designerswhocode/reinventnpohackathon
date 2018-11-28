import json
import boto3
import uuid
import datetime

def invokeSteps(event):
    client = boto3.client('stepfunctions','us-east-1')
    response = client.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:751485721275:stateMachine:JobStatusPollerStateMachine-7jRdbIecvj7y',
        name=str(uuid.uuid1()),
        input=json.dumps(event)
    )

def lambda_handler(event, context):
    # TODO implement
    username = event['pathParameters']['username']
    jsonBody = json.loads(event['body'])

    if (jsonBody['type'] == "voice"):
        invokeSteps({
            "from_user": username,
            "to_user": jsonBody['to_user'],
            "timestamp": datetime.datetime.now().timestamp(),
            "wait_time": 15,
            "file_name": jsonBody['message']
            }
        )
    else:    
        client = boto3.client('lambda')
        
        client.invoke(
            FunctionName = "arn:aws:lambda:us-east-1:751485721275:function:message_delivery_preprocess",
            InvocationType='RequestResponse',
            Payload = json.dumps({
                "from_user": username,
                "to_user": jsonBody['to_user'],
                "timestamp": datetime.datetime.now().timestamp(),
                "status": {
                    "transcript": jsonBody['message']
                }
            })
        )
    
    
    return {
        'statusCode': 200,
        'body': "{}"
    }
