import json
import os
import boto3

def handler(event, context):
    queue_url = os.environ.get('QueueURL')
    top_movies_bucket = os.environ.get('MoviesBucket')

    # S3 and SQS clients (modify queue URL if sending to SQS)
    s3 = boto3.client('s3') 
    sqs = boto3.client('sqs')

    

    


    
    