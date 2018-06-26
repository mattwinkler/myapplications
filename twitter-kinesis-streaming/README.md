
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

`import boto3  
client = boto3.client(
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


