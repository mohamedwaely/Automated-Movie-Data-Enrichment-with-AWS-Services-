import json
import os
import boto3

def handler(event, context):
    # using the environment variables
    # queue_url
    queue_url = os.environ.get('QueueURL')

    # S3 and SQS clients
    s3 = boto3.client('s3', 'eu-central-1')
    sqs = boto3.client('sqs')

    # Bucket and object details
    bucket_name = 'top-movies'
    object_name = 'Top250Movies.json'

    try:
        # Get the S3 object
        response = s3.get_object(Bucket=bucket_name, Key=object_name)

        # Decode and load JSON data
        movies_data = json.loads(response['Body'].read().decode('utf-8'))
        top_10_items = movies_data['items'][:10]

        # Send message to SQS
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(top_10_items)
        )

        # Success message
        print(f"Successfully sent top 10 items from {object_name} to SQS.")
        return {
            'statusCode': 200,
            'body': json.dumps(f'{top_10_items}')
        }

    except Exception as e:
        # Handle any exceptions during processing
        print(f"Error processing data: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing data: {e}")
        }
