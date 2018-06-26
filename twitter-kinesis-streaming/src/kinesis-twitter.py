
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boto3
import json
import twittercreds
import settings

appconfigs = settings.appconfigs

# twitter credentials:
consumer_key = twittercreds.consumer_key
consumer_secret = twittercreds.consumer_secret
access_token_key = twittercreds.access_token_key
access_token_secret = twittercreds.access_token_secret

# boto connection to kinesis:
KINESIS_CLIENT = boto3.client('kinesis')

# Read list of terms to track in Twitter Stream:
TERM_LIST = appconfigs['TWITTER']['search_terms'].split(',')

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    Tweets are added to the tweets attribute as they arrive.
    """
    def __init__(self):
        self.tweets = []
        self.count = 0
        self.partition_key = appconfigs['AWS-KINESIS']['partition_key']

    def on_data(self, data):
        #pdb.set_trace()
        #json_item = json.dumps(data)
        self.tweets.append({'Data': data, 
                            'PartitionKey': self.partition_key})
        self.count += 1
        # flush data to Kinesis when the tweet count reaches 100:
        if self.count == 100:
            KINESIS_CLIENT.put_records(StreamName=appconfigs['AWS-KINESIS']['stream_name'], 
                            Records=self.tweets)
            self.tweets = []
            self.count = 0

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=TERM_LIST)