import json
import os
import boto3
from urllib.parse import urlencode
import urllib3

def handler(event, context):
    # using the environment variables
    # queue_url
    queue_url = os.environ.get('QueueURL')
    # bucket name
    top_movies_bucket_name = os.environ.get('MoviesBucket')
    # OMDB API key
    api_key = os.environ.get('OMDB_API_KEY')

    # S3 and SQS clients
    sqs_client = boto3.client('sqs')
    s3_client = boto3.client('s3','eu-north-1')
    # print(event)
    
    try:
        # message_body = event['Records'][0]['body']
        # movies = json.loads(message_body)

        recs = event['Records']

        updated_movies_list=[]

        for rec in recs:
            imdb_id = rec["id"]
            api_url = f"https://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"
            
            # Use urllib3 to make the GET request
            http = urllib3.PoolManager()
            response = http.request('GET', api_url)
        
             # Check for successful response
            if response.status == 200:
                # Parse the JSON response
                response_data = json.loads(response.data.decode('utf-8'))
                # Update movie object with additional data
                rec.update(response_data)
                updated_movies_list.append(rec)
            else:
                # Handle failed request (e.g., log the error)
                print(f"Error: API request failed with status code {response.status}")
            # Delete received message from queue
            receipt_handle = rec.get('ReceiptHandle')
            if receipt_handle:
                sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

        # Store enriched data in the Bucket
        s3_client.put_object(Bucket=top_movies_bucket_name, Key="top_ten_enriched_movies.json", Body=json.dumps(updated_movies_list))

        # print the size of the message body
        print(f"Received and processed")

    except json.JSONDecodeError:
        # Handle potential error if the message body isn't valid JSON
        return {
                'statusCode': 200,
                'body': (print("Error: Invalid JSON format in message body."))
        }

