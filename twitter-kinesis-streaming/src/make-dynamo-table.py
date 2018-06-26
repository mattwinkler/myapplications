## create a table to store twitter hashtags in DynamoDB
import boto3
import settings
import pdb

appconfigs = settings.appconfigs

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName=appconfigs['AWS-DYNAMO']['table_name'],
    KeySchema=[
        {
            'AttributeName': 'hashtag',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'hashtag',
            'AttributeType': 'S'
        }
    ],
    # pricing determined by ProvisionedThroughput
    ProvisionedThroughput={
        'ReadCapacityUnits': int(appconfigs['AWS-DYNAMO']['read_capacity']),
        'WriteCapacityUnits': int(appconfigs['AWS-DYNAMO']['write_capacity'])
    }
)

table.meta.client.get_waiter('table_exists').wait(TableName=appconfigs['AWS-DYNAMO']['table_name'])