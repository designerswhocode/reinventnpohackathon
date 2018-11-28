# system
import sys
import logging
import datetime
import json
import boto3

# project
import rds_config

# libraries
import psycopg2
from psycopg2.extras import RealDictCursor

# rds settings
rds_host = "awshack.cm7uciaprqlt.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    connection = psycopg2.connect(host=rds_host, user=name, password=password, database=db_name)
except Exception as e:
    logger.error(e)
    sys.exit()

SQL_IS_USER_BANNED = """
    SELECT * FROM blacklist WHERE user = %s
"""

SQL_FLAGGED_MESSAGES_FOR_USER = """
    SELECT * FROM messages WHERE from_user = %s AND is_flagged = TRUE
"""

SQL_BAN_USER = """
    INSERT INTO blacklist(user) VALUES(%s) ON CONFLICT(user) DO NOTHING
"""

SQL_INSERT_MESSAGE = """
    INSERT INTO messages(from_user, to_user, message, timestamp, is_flagged) VALUES(%s, %s, %s, %s, %s)
"""

SQL_SELECT_LANGUAGE_FOR_USER = """
    SELECT * FROM languages WHERE "user" = %s
"""

def translate(text,target):
    if(target=='fr'):
        source='en'
    else:
        source='fr'
    trans_client = boto3.client('translate','us-east-1')
    response = trans_client.translate_text(
        Text=text,
        SourceLanguageCode=source,
        TargetLanguageCode=target
    )
    print(response['TranslatedText'])
    return response['TranslatedText']

def detect(text):
    if "high" in text: 
        return True
    else:
        return False
        
def handler(event, context):
    cursor: RealDictCursor = connection.cursor(cursor_factory=RealDictCursor)
    

    fromUser = event['from_user']
    toUser = event['to_user']
    message = translate(event['status']['transcript'], 'en')
    timestamp = event['timestamp']
    isFlagged = detect(message)
    
    cursor.execute(SQL_IS_USER_BANNED, (fromUser,))
    
    if (cursor.rowcount == 0):
        if (isFlagged):
            # First we check if user is banned
            cursor.execute(SQL_FLAGGED_MESSAGES_FOR_USER, (fromUser,))
            
            if (cursor.rowcount > 1):
                # ban the user
                cursor.execute(SQL_BAN_USER, (fromUser,))
            
            # Insert the message        
            cursor.execute(SQL_INSERT_MESSAGE, (fromUser, toUser, message, datetime.datetime.fromtimestamp(timestamp), isFlagged))
            connection.commit()
        else:
            # we translate the message to kids language and save it to DB
            cursor.execute(SQL_SELECT_LANGUAGE_FOR_USER, (toUser,))
            if (cursor.rowcount == 0):
                translatedMessage = message
            else:
                languageRecord = cursor.fetchone()
                print(languageRecord['language'])
                translatedMessage = translate(message, languageRecord['language'])
                
            # Insert the message        
            cursor.execute(SQL_INSERT_MESSAGE, (fromUser, toUser, translatedMessage, datetime.datetime.fromtimestamp(timestamp), isFlagged))
            connection.commit()
           


    cursor.close()

    return {
        "statusCode": 200,
        "body": json.dumps({})
    }

