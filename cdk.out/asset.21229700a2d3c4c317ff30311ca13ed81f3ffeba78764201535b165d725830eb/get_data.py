import json
import os
import boto3

def handler(event, context):
    queue_url = os.environ.get('QueueURL')

        # S3 and SQS clients (modify queue URL if sending to SQS)
    s3 = boto3.client('s3', 'eu-central-1')  # Update region if necessary
    sqs = boto3.client('sqs')  # Optional for sending to SQS

        # Bucket and object details
    bucket_name = 'top-movies'
    object_name = 'Top250Movies.json'

    
        # Get the S3 object
    response = s3.get_object(Bucket=bucket_name, Key=object_name)

        # Decode and load JSON data
    movies_data = json.loads(response['Body'].read().decode('utf-8'))
    top_10_items=movies_data['items'][:10]
    
    sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(top_10_items,
        )
    )
    
    # return {
    #     'statusCode': 200,
    #         'body': json.dumps(f'{top_10_items}')
    # }