
"""
This module contains the logic for translating S3 paths to 
the format needed to execute batch transformation jobs 
"""

import json
import re
from urllib.parse import unquote

def parse_event(event):
	""" Identifies file to get from incoming event record """
	print("Parsing event")
	try:
		records = event.get("Records", [])
		if len(records) > 0:
			record = records[0]
				
		#region = record.get("awsRegion", "")
		#extracts the JSON relevant information for variable population
		s3data = record.get("s3", {})
		print(s3data)
		bucket = s3data.get("bucket", {})
		bucket_name = bucket.get("name", "")
		object_data = s3data.get("object", {})
		object_key = object_data.get("key", "")
		#object_key = unquote_plus(object_key) ## Remove "+" from json event
		return bucket_name, object_key
	except Exception as e:
		print("parse_event: {}".format(e))
		raise e

def get_input_path(bucket, object_key):
    """Identifies the facility_code, and run_date embedded in the S3 path"""
    # first find the filename as the last part of the path, using / as a delimiter
    object_key = unquote(object_key)
    print('object key: {}'.format(object_key))
    return 's3://{}/{}'.format(bucket, object_key)

def get_output_path(bucket, output_prefix):
    """Maps path variables into a new S3 URL to store predictions"""
    output_path = 's3://' + '/'.join([bucket, output_prefix])
    return output_path

def write_log_file(s3_client, bucket, logging_key, model_name):
    """Write the model used to generate the predictions to the logging path. This provides insight into which 
    model version was used to generate predictions on a given date"""
    json_data = {"model_name": model_name}
    log_file = 'transform_log.json'
    tmp_path = '/tmp/{}'.format(log_file)
    logging_key += '/{}'.format(log_file)
    with open(tmp_path, 'w') as output_file:
        output_file.write(json.dumps(json_data))
    
    s3_client.upload_file(tmp_path, bucket, logging_key)
    return logging_key