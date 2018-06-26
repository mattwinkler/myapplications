## script to read data from Kinesis, extract hashtags and store into 
## dynamoDB

import boto3
import time
import json
import decimal
import settings

appconfigs = settings.appconfigs

## Connent to the kinesis stream
kinesis = boto3.client("kinesis")
shard_id = 'shardId-000000000000' #only one shard
shard_it = kinesis.get_shard_iterator(StreamName=appconfigs['AWS-KINESIS']['stream_name'], 
    ShardId=shard_id, 
    ShardIteratorType="LATEST")["ShardIterator"]

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(appconfigs['AWS-DYNAMO']['table_name'])

while 1==1:
    out = kinesis.get_records(ShardIterator=shard_it,
         Limit=100)
    for record in out['Records']:
        record_data = json.loads(record['Data'])
        if record_data['truncated']: # longer tweets have extended_entities
            entities = record_data.get('extended_entities', {})
        else:
            entities = record_data.get('entities', {})
        htags = entities.get('hashtags', None)
        if htags:
            for ht in htags:
                htag = ht['text']
                checkItemExists = table.get_item(
                            Key={
                                    'hashtag':htag
                            }
                    )
                    
                if 'Item' in checkItemExists:
                    response = table.update_item(
                            Key={
                                'hashtag': htag 
                                },
                            UpdateExpression="set htCount  = htCount + :val",
                            ConditionExpression="attribute_exists(hashtag)",
                            ExpressionAttributeValues={
                                ':val': decimal.Decimal(1)
                                },
                            ReturnValues="UPDATED_NEW"
                            )
                else: 
                    response = table.update_item(
                            Key={
                                'hashtag': htag
                                },
                            UpdateExpression="set htCount = :val",
                            ExpressionAttributeValues={
                                ':val': decimal.Decimal(1)
                                },
                            ReturnValues="UPDATED_NEW"
                                        )    
    shard_it = out["NextShardIterator"]
    time.sleep(1.0)