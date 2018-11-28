import boto3
import uuid
import json


def translate(text):
    trans_client = boto3.client('translate','us-east-1')
    response = trans_client.translate_text(
        Text=text,
        SourceLanguageCode='fr',
        TargetLanguageCode='en'
    )
    print(response['TranslatedText'])
    return response['TranslatedText']

def flat_messages(text):
    if "high" in text: 
        return True
    else:
        return False

def run(event, context):
    print(event)
    english_text=translate(event)
    return flat_messages(english_text)

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
