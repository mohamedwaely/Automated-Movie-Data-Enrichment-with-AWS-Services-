import json
import os
import boto3

def handler(event, context):
    queue_url = os.environ.get('QueueURL')
    top_movies_bucket_name = os.environ.get('MoviesBucket')

    # S3 and SQS clients (modify queue URL if sending to SQS)
    sqs_client = boto3.client("sqs")
    s3_client = boto3.client("s3")

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )


    # Check if message is received
    if "Messages" in response:
        message = response["Messages"][0]
        receipt_handle = message["ReceiptHandle"]
        message_body = json.loads(message["Body"])  # Convert string to dictionary/list

        # Loop through movies in message_body list(Array)
        api_key = "7c1b607f"
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
        print(f"Received and processed {len(message_body)} movies.")
    else:
        return {
                'statusCode': 200,
                'body': f'No Messages in Queue'
            }

return {
          'statusCode': 300,
          'body': 'Processed SQS message.'
}