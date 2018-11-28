import boto3
import uuid
import json

def getTranscript(jobname):
    s3_client = boto3.client('s3','us-east-1')
    response = s3_client.get_object(
        Bucket='npohackathon',
        Key=jobname+'.json'
    )
    file_content = response['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    print(json_content['results']['transcripts'][0]['transcript'])
    return json_content['results']['transcripts'][0]['transcript']


def run(event, context):
    client = boto3.client('transcribe','us-east-1')
    print(event)
    jobname=event
    response = client.get_transcription_job(
        TranscriptionJobName=jobname
    )
    
    transcription=response['TranscriptionJob']

    status=transcription['TranscriptionJobStatus']
    print(status)
    if(status == 'COMPLETED'):
        transcript=getTranscript(jobname)
        print(transcript)
    else:
        transcript=None

    return {
        "status":status,
        "transcript":transcript
    }

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
