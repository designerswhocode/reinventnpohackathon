import boto3
import uuid
import json


def run(event, context):
    client = boto3.client('transcribe','us-east-1')
    jobname=str(uuid.uuid1())
    response = client.start_transcription_job(
        TranscriptionJobName=jobname,
        LanguageCode='fr-CA',
        MediaSampleRateHertz=44100,
        MediaFormat='mp3',
        Media={
            'MediaFileUri': 'https://s3-us-east-1.amazonaws.com/npohackathon/'+event
        },
        OutputBucketName='npohackathon'
    )

    return jobname

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
