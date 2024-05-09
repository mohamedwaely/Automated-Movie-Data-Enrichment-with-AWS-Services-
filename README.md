<h2>Lambda and Stacks Files in the _dyra_task directory</h2>
<h3>Firstly, We will start with _dyra_task_stack.py file to build the AWS tools and each tool will explain its usage..
(in our project SQS Queue, S3 bucket, and Two lambda Functions each function in a directory)</h3>


<h4>Dive into this Stack:</h4>

Create the SQS Queue and store the URL of this queue in the ENVIRONMENT VARIABLES by using AWS CLI or the AWS Console.



Create the S3 Bucket that we will use to upload or Store the object file which will contain the TOP_10_FILTERED_MOVIES, 
also, we will store the Bucket Name in the ENVIRONMENT VARIABLES by using AWS CLI or the AWS Console.

<h3>The Next Two Lambda functions in the directory /_dyra_task/first_lambda_fun/ and /_dyra_task/second_lambda_fun/</h3>

 Create the <h4>First Lambda function (get_data.py) that will get the data from the given s3 bucket and filter the top 10 movies:</h4>
  First things we will import the queue_url from the os environ class.
 ```
  (given in the task description: https://top-movies.s3.eu-central-1.amazonaws.com/Top250Movies.json),
```
 After that get the Top250Movies.json 
 from the Bucket and loads it, filter the TOP_10 movies based on the movie_rank, and send messages to the SQS Queue which includes this object body (Send Messages One by One).

 <h4>Once we send messages to the SQS Queue, it will INVOKE the second Lambda function (enrich_data.py) By Using Event Source that enables serverless processing of incoming data. 
  This creates a scalable and event-driven architecture for data enrichment tasks</h4>
  
  ```
      This Code From the _dyra_task_stack.py explains what i mean:
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
  ```
 
 Before explaining this lambda function we should store the OMDB_API_KEY in the ENVIRONMENT VARIABLES for security by using this command:
 ```
  aws lambda update-function-configuration \
  --function-name enrich_data_lambda \
  --environment Variables="{OMDB_API_KEY: {The Real Key} }"
 ```

 First things we will import the queue_url, s3_bucket_name, and the OMDB_API_KEY from the os environ class.
 
 Then get the event Records (this refers to the messages we sent to the SQS Queue which contains the Top_10_Movies)
 and loops through the Records to enrich each movie by using IMDB_Id and urllib3 for API calls.
 
 After updating the top_10_movies we will store the object in the s3_bucket, then delete the message from the SQS Queue.

 <h2>Lastly In the app.py we will call the _dyra_task_stack class</h2>



# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
