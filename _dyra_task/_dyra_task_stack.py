from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_sqs as sqs,
    aws_s3 as s3,
    CfnOutput,
    aws_lambda as _lambda,
)
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from constructs import Construct
import os
class DyraTaskStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create the Queue that will send and receive the messages
        movie_enrichment_queue=sqs.Queue(
            self, "top-movies-queue",
            visibility_timeout=Duration.seconds(300),
        )

        # Get the queue URL
        queue_url = movie_enrichment_queue.queue_url
        # Define output for the queue_url queue (store the queue_url in the environment variables)
        # CfnOutput(self, id="SQSQueueURL", value=queue_url, export_name="QueueUrl")

        # determine the current directory to use it to intialize the lambda functions
        current_dir = os.path.dirname(__file__)

        # Specify the first Lambda code directory 
        first_lambda_code_dir = os.path.join(current_dir, "first_lambda_fun")

        # create the first lambda function that will get the data from the given s3 bucket
        get_data_lambda = _lambda.Function(
            self,
            "GetData",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(first_lambda_code_dir),  # Use the directory path
            handler="get_data.handler",
        )

        # create the s3 bucket that we will store the Enriched data in it
        enrich_movies_bucket = s3.Bucket(
            self, "MoviesBucket"
        )
        # determine the bucket name that we are created to store the data
        bucket_name = enrich_movies_bucket.bucket_name

        # Define output for the S3 bucket name (store the bucket in the environment variables)
        # CfnOutput(self, "movies_bucket", value=bucket_name, export_name="MoviesBucket")

        # Specify the first Lambda code directory 
        second_lambda_code_dir = os.path.join(current_dir, "second_lambda_fun")

        # create the second lambda function that will enrich the data that are stored in the Queue,...etc
        enrich_data_lambda = _lambda.Function(
            self,
            "EnrichData",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(second_lambda_code_dir),  # Use the directory path
            handler="enrich_data.handler",
        )

        """
            This CDK code utilizes an SQS event source to trigger the EnrichData Lambda function. 
            When a message arrives in the top-movies-queue, 
            the event source automatically invokes the Lambda function, 
            enabling serverless processing of incoming data. 
            This creates a scalable and event-driven architecture for data enrichment tasks.
        """
        event_source = SqsEventSource(movie_enrichment_queue)
        enrich_data_lambda.add_event_source(event_source)

        event_source_id = event_source.event_source_mapping_id






