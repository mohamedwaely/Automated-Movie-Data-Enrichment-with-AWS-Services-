import json
import os
import boto3
from urllib.parse import urlencode
import urllib3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    Processes messages from an SQS queue containing movie IDs in batches, fetches additional data from OMDB API for each movie,
    merges the data, and stores all enriched movie data in an S3 bucket after processing the entire batch.
    
    """

    # Retrieve environment variables
    queue_url = os.environ.get('QueueURL')
    movies_bucket_name = os.environ.get('BucketName')
    omdb_api_key = os.environ.get('OMDB_API_KEY')

    # SQS and S3 clients
    sqs_client = boto3.client('sqs')
    s3_client = boto3.client('s3', 'eu-north-1')

    enriched_movies = []

    try:
        for record in event['Records']:
            try:
                # Parse the SQS message body as JSON
                movie_data = json.loads(record['body'])
                movie_id = movie_data['id']

                # Build API URL with retrieved API key
                api_url = f"https://www.omdbapi.com/?apikey={omdb_api_key}&i={movie_id}"

                # Make API request and handle errors
                http = urllib3.PoolManager()
                response = http.request('GET', api_url)
                if response.status == 200:
                    api_data = json.loads(response.data.decode('utf-8'))

                    movie_data = api_data

                    # Add the enriched movie data to the list
                    enriched_movies.append(movie_data)
                    # print(len(enriched_movies))

                else:
                    logger.error(f"API request failed for movie ID: {movie_id} (status code: {response.status})")

            except json.JSONDecodeError as e:
                logger.error(f"Error parsing message body (record {record['messageId']}): {e}")

            except Exception as e:
                logger.error(f"Unexpected error processing movie ID: {movie_id}", exc_info=True)

    except KeyError as e:
        logger.error(f"Missing required environment variable: {e}")
        # Handle missing environment variables

    # Store enriched data in S3 bucket after processing all messages in the batch
    if enriched_movies:
        s3_client.put_object(
            Bucket=movies_bucket_name,
            Key="top_ten_enriched_movies.json",
            Body=json.dumps(enriched_movies)
        )
        logger.info(f"Processed {len(enriched_movies)} movies and stored enriched data in S3.")

    # Delete processed messages from SQS queue
    for record in event['Records']:
        receipt_handle = record.get('ReceiptHandle')
        if receipt_handle:
            sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

