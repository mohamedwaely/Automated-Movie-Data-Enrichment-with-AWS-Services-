import json
import os
import boto3

def handler(event, context):
    queue_url = os.environ.get('QueueURL')
    top_movies_bucket_name = os.environ.get('MoviesBucket')

    # S3 and SQS clients (modify queue URL if sending to SQS)
    sqs_client = boto3.client("sqs")
    s3_client = boto3.client("s3")
    try:
        movies = json.loads(message_body = event['Records'][0]['body'])
        api_key = "7c1b607f"
        # Loop through movies in message_body
        for movie in message_body:
            imdb_id = movie["id"]
            api_url = f"https://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"
            response = json.loads(requests.get(api_url).text)

            # Update movie object with additional data (modify as needed)
            movie.update(response)

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

