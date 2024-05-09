import json
import os
import boto3

def handler(event, context):
    # using the environment variables
    # queue_url
    queue_url = os.environ.get('QueueURL')
    # bucket name
    top_movies_bucket_name = os.environ.get('MoviesBucket')
    # OMDB API key
    api_key = os.environ.get('OMDB_API_KEY')

    # S3 and SQS clients
    sqs_client = boto3.client("sqs")
    s3_client = boto3.client("s3")
    message_body
    try:
        message_body = event['Records'][0]['body']
        movies = json.loads(message_body)
    # Use boto3 client for API call
        client = boto3.client('http')

        for movie in movies:
            imdb_id = movie["id"]
            api_url = f"https://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"

            # Define request parameters
            response = client.get(
                url=api_url
            )

            # Check for successful response
            if response['StatusCode'] == 200:
                response_data = json.loads(response['Body'].read())
                movie.update(response_data)
            else:
                # Handle API call error
                print(f"Error: API call failed with status code {response['StatusCode']}")

        # Store enriched data (logic can be modified)
        s3_client.put_object(Bucket=top_movies_bucket_name, Key="top_ten_enriched_movies.json", Body=json.dumps(message_body))

        # Delete received message from queue (unchanged)
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        # print the size of the message body
        print(f"Received and processed {len(message_body)} movies.")

    except json.JSONDecodeError:
        # Handle potential error if the message body isn't valid JSON
        return {
                'statusCode': 200,
                'body': (print("Error: Invalid JSON format in message body."))
        }

