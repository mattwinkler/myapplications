
# Sources:

This project was built on top of two excellent resources:  

1) Daniel Blazevski's tutorial, which provided the basic framework:  
https://blog.insightdatascience.com/getting-started-with-aws-serverless-architecture-tutorial-on-kinesis-and-dynamodb-using-twitter-38a1352ca16d

2) Kyran Dale's Data Visualization with Python and Javascript, which I referenced to set up the stream listener using Tweepy.  You can find a copy of his book here:  http://shop.oreilly.com/product/0636920037057.do

# Introduction:  

This application uses Python and AWS to create a Twitter streaming app with Amazon Kinesis and DynamoDB.  As of 6/26/2018, the application ingests data and stores hashtags associated with a set of search terms specified by the user.  Future iterations will build out the DynamoDB schema more fully and apply Natural Language Processing concepts to the backend.  

# Prerequisites  

* Python 3.6 installed
* Install libraries from `requirements.txt`:  

`pip install -r requirements.txt`  

* AWS account created
* Twitter developer account (go to https://apps.twitter.com)

# Setup:

First clone this repository: `https://github.com/mattwinkler/myapplications/tree/master/twitter-kinesis-streaming`

### AWS:

Option 1) If you have the AWS CLI installed (https://aws.amazon.com/cli/), you can run `aws configure` to set up your access credentials.  

Option 2) It's also possible to specify your access keys for an individual connection without setting the defaults.  It's recommended to save the keys themselves in an environment variable so they aren't accidentally committed to a public repository.  See example below:  

`import boto3`

`client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
)`

### Twitter:

Use the link above to set up your Twitter developer account.  You will need to save the values for the following variables in a secure location:  

* access_token_key
* access_token_secret
* consumer_key
* consumer_secret

This application assumes that these values are stored in environment variables on the host system.  For reference, they're read into the app in the `twittercreds.py` script.

### Application:

Update the `config.ini` file as-needed to meet your application's requirements.  The file has four sections representing each function of the application:

* [TWITTER]: Which terms to search for in the Twitter stream listener
* [AWS-KINESIS]: Name of the Kinesis stream to create, shard count, and stream partitiions
* [AWS-DYNAMO]: Name of the DynamoDB table where stream data will live and associated read / write parameters
* [AWS-TAGS]: Tags and values to attach to resources created in AWS.

# Creating Resources:

### Kinesis:

To begin with, run `make-stream.py`.  If everything is set up correctly, you should be able to see the stream with the name specified in the [AWS-KINESIS] section of `config.ini`.  

### DynamoDB:

Next run `make-dynamo-table.py`.  This will create the DynamoDB table to house data from the Kinesis stream and specify the partition key for that table.

# Populating data tables:

Almost there!  There are two python applications that must be running for the DynamoDB table to update:

`kinesis-twitter.py`  
`kinesis-dynamo.py`

Hint: Run each script in a separate terminal window.  Once everything is running, you should be able to see the DynamoDB table updating within the AWS Console.  

# Analysis:

See outputs in the `viz/` folder.

The current version of this application uses a Jupyter Notebook running in an AWS Sagemaker instance for the analysis step. Future iterations will capture richer data and apply more sophisticated techniques to it.  To run the same analysis locally instead of in Sagemaker, install anaconda `pip install anaconda`.

