# -*- coding: utf-8 -*-
"""
This script contains logic to orchestrate batch transformation jobs based on data objects created in the 
analytics bucket. The s3_functions and batch_transform_functions imports are local modules designed
to separate logic used across scripts, increasing long term maintainability.
"""

import boto3
import botocore
import json
import os
from datetime import datetime
from time import strftime

from batch_transform_functions import *

RUN_TIME = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

# Get local environment variables:
try:
    BATCH_JOB_NAME = os.getenv('BATCH_JOB_NAME', '')
    OUTPUT_PREFIX = os.getenv('OUTPUT_PREFIX', '')
    TRAINED_MODEL_PREFIX = os.getenv('TRAINED_MODEL_PREFIX', '')
    MODEL_NAME_VERSION = os.getenv('MODEL_NAME_VERSION', '')
    INSTANCE_TYPE = os.getenv('INSTANCE_TYPE', '')

    ORG = os.getenv('ORG', '')
    ENVIRONMENT = os.getenv('ENVIRONMENT', '')
    APPNAME = os.getenv('APPNAME', '')
    APPID = os.getenv('APPID', '')
    OWNER_EMAIL_DIST = os.getenv('OWNER_EMAIL_DIST', '')
    COST_CENTER_NUMBER = os.getenv('COST_CENTER_NUMBER', '')

except Exception as e:
    print('Problem executing batch transform')
    print('Error description: {}'.format(e))
    print('BATCH_JOB_NAME: {}'.format(BATCH_JOB_NAME))
    print('OUTPUT_PREFIX: {}'.format(OUTPUT_PREFIX))
    print('TRAINED_MODEL_PREFIX: {}'.format(TRAINED_MODEL_PREFIX))
    print('MODEL_NAME_VERSION: {}'.format(MODEL_NAME_VERSION))
    
    print('ORG: {}'.format(ORG))
    print('ENVIRONMENT: {}'.format(ENVIRONMENT))
    print('APPNAME: {}'.format(APPNAME))
    print('APPID: {}'.format(APPID))
    print('OWNER_EMAIL_DIST: {}'.format(OWNER_EMAIL_DIST))
    print('COST_CENTER_NUMBER: {}'.format(COST_CENTER_NUMBER))

# create the skeleton of the Sagemaker API request, with parameters updated at runtime:
# ModelName: Mapped from the stage embedded in the input data file parsed from the event
# S3Uri: Represents the input location for running predictions from Sagemaker. S3 path of the file that triggered the lambda event when it was created
# S3OutputPath: Mapped from the OUTPUT_PREFIX environment variable and the stage name

request = \
{
    "TransformJobName": "",                   ####### mapped at runtime
    
    "ModelName": "",                          ####### mapped at runtime
    
    "MaxConcurrentTransforms": 4,
    "MaxPayloadInMB": 6,
    "BatchStrategy": "MultiRecord",
    "TransformOutput": {
        
        "S3OutputPath": ""                    ####### mapped at runtime
    
    },
    "TransformInput": {
        "DataSource": {
            "S3DataSource": {
                "S3DataType": "S3Prefix",
                
                "S3Uri": ""                   ####### mapped at runtime
            
            }
        },
        "ContentType": "text/csv",
        "SplitType": "Line",
        "CompressionType": "None"
    },
    "TransformResources": {
            "InstanceType": INSTANCE_TYPE,
            "InstanceCount": 1
    },
    "Tags": [ 
       { 
         "Key": "Org",
         "Value": ORG
       },
       { 
         "Key": "Environment",
         "Value": ENVIRONMENT
       },
       { 
         "Key": "Appname",
         "Value": APPNAME
       },
       { 
         "Key": "AppId",
         "Value": APPID
       },
       { 
         "Key": "OwnerEmailDist",
         "Value": OWNER_EMAIL_DIST
       },
       { 
         "Key": "CostCenterNumber",
         "Value": COST_CENTER_NUMBER
       }
   ]
}

# start the sagemaker client
sm = boto3.client('sagemaker')
s3 = boto3.client('s3')

def format_request(request, batch_job_name, run_time, input_path, output_path, model_name):
    """Updates the request skeleton with input_path, output_path, and model_name created 
    at runtime in this lambda function"""
    job_name = '-'.join([batch_job_name, run_time])
    request['TransformJobName'] = job_name
    request['ModelName'] = model_name
    request['TransformInput']['DataSource']['S3DataSource']['S3Uri'] = input_path
    request['TransformOutput']['S3OutputPath'] = '/'.join([output_path, model_name, run_time])
    return request, job_name

def lambda_handler(event, context):
    print(event)
    bucket, object_key = parse_event(event)
    try:
    
        input_path = get_input_path(bucket, object_key)
    
        output_path = get_output_path(bucket=bucket,
                                      output_prefix=OUTPUT_PREFIX)
        
        formatted_request, job_name = format_request(request=request, 
                                           batch_job_name=BATCH_JOB_NAME,
                                           run_time=RUN_TIME,
                                           input_path=input_path, 
                                           output_path=output_path, 
                                           model_name=MODEL_NAME_VERSION)
        
        print('sagemaker request: {}'.format(str(formatted_request)))
        
        print('script run time: {}'.format(RUN_TIME))
        
        print('prediction output path: {}'.format(output_path))
    
        # Execute the batch transformation with the completed request
        sm.create_transform_job(**formatted_request)
        
        print("Created Transform job: ", job_name)
        
    except Exception as e:
        print(e)
        print('Job Name: {}'.format(job_name))
        print('Model Name: {}'.format(trained_model_name))
        print('Data input path: {}'.format(input_path))
        print('Data output path: {}'.format(output_path))
        raise e
        
    # predictions_exist = False
    # continue_search = True
    # while continue_search:
    #     try:
    #         response = s3.list_objects_v2(Bucket=bucket, Prefix=output_key)
    #         if len(response['Contents']) > 0:
    #             predictions_exist = True
    #             print('found existing prediction file')
    #             logging_key = write_log_file(s3_client=s3, 
    #                                  bucket=bucket, 
    #                                  logging_key=logging_key, 
    #                                  model_name=trained_model_name)
    #             print('logging_key = {}'.format(logging_key))
    #             continue_search = False

    #     except Exception as e: # key doesn't exist within the bucket. Continue searching.
    #         if e.__class__.__name__ == 'KeyError':
    #             continue
    #         else:
    #         # Something else has gone wrong.
    #             raise e
    return {"status": 200}