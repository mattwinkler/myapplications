## Introduction to AWS Sagemaker

This repository contains the infrastructure demo'd during the April 25 meeting of the Chicago ML meetup (https://www.meetup.com/Chicago-ML/), including the following components:  

* `cft`: Cloudformation templates to deploy the stack used for this demo  
* `lambda`: Python code to trigger batch transformation jobs when files are uploaded to the analytics subfolder of the target S3 bucket  

## Deploying the Stack

#### AWS Services Used  

* S3: `code` and `analytics` buckets  
* Sagemaker: Data scientists can use the notebook  
* Lambda: Triggers Sagemaker batch transformation jobs when data is uploaded to the `data/predict` path of the analytics bucket

#### Prerequisites  

* AWS CLI installed  
* AWS Access Key and Secret Access Key  
* IAM permissions for resources used  

#### Deployment Steps

Within the `cft` folder are the templates for each service deployed in the stack. The `build.txt` file contains AWS CLI commands, in the order listed, to deploy. You will also need to include the `--profile` and `--region` variables in the command.   

TODO: Write one script to deploy all resources