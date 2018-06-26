
import boto3
import settings

appconfigs = settings.appconfigs

KINESIS_CLIENT = boto3.client('kinesis')

response = KINESIS_CLIENT.create_stream(
   StreamName=appconfigs['AWS-KINESIS']['stream_name'],
   ShardCount=int(appconfigs['AWS-KINESIS']['shard_count'])
)

print('creation response status: ', response['ResponseMetadata']['HTTPStatusCode'])
print('creation response:' , response)

response = KINESIS_CLIENT.add_tags_to_stream(
    StreamName=appconfigs['AWS-KINESIS']['stream_name'],
    Tags = {
        'Owner': appconfigs['AWS-TAGS']['owner'],
        'Manager': appconfigs['AWS-TAGS']['manager'],
        'Email': appconfigs['AWS-TAGS']['email'],
        'Location': appconfigs['AWS-TAGS']['location'],
        'Engagement Office': appconfigs['AWS-TAGS']['engagement_office']
    }
)

print('tagging response status: ', response['ResponseMetadata']['HTTPStatusCode'])
print('tagging response', response)