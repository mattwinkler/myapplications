
import boto3
import time
import json
import settings

appconfigs = settings.appconfigs

kinesis = boto3.client('kinesis')
shard_id = "shardId-000000000000" #only one shard!
pre_shard_it = kinesis.get_shard_iterator(StreamName=appconfigs['AWS-KINESIS']['stream_name'], 
           ShardId=shard_id, 
           ShardIteratorType="LATEST")
shard_it = pre_shard_it["ShardIterator"]
while 1==1:
     out = kinesis.get_records(ShardIterator=shard_it, Limit=1)
     shard_it = out["NextShardIterator"]
     print(out)
     time.sleep(1.0)