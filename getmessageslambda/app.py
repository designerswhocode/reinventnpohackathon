# system
import sys
import logging
#import datetime
import json

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

SQL_GET_MESSAGES_FOR_USER = """
    SELECT * FROM messages WHERE to_user = %s AND is_flagged = FALSE
"""

def handler(event, context):
    cursor: RealDictCursor = connection.cursor(cursor_factory=RealDictCursor)

    username = event['pathParameters']['username']

    cursor.execute(SQL_GET_MESSAGES_FOR_USER,  (username,))
    
    result = []
    
    if (cursor.rowcount > 0):
        messages = cursor.fetchall()
        
        for message in messages:
            result.append({
                "from_user": message['from_user'],
                "to_user": message['to_user'],
                "message": message['message'],
                "timestamp": message['timestamp'].timestamp()
            })

    cursor.close()

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }

