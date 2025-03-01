import json
import boto3
import os
from datetime import datetime

# AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# DynamoDB table
table = dynamodb.Table('ImageMetadataTable')

def lambda_handler(event, context):
    # Get bucket name and object key from event
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        # Get object metadata
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        file_size = response['ContentLength']
        upload_time = response['LastModified'].isoformat()
        
        # Store metadata in DynamoDB
        table.put_item(Item={
            'filename': object_key,
            'bucket': bucket_name,
            'size_in_bytes': file_size,
            'upload_time': upload_time
        })

    return {
        'statusCode': 200,
        'body': json.dumps('Metadata stored successfully!')
    }
