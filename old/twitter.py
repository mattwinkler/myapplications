# https://mw_streams.info

from __future__ import print_function
import tweepy
from tweepy.streaming import StreamListener
import json
import mongo_connector as mongo


class TwitterReader():
    def __init__(self, credentials_file_name):
        self.credentials_file_name = credentials_file_name
        with open(self.credentials_file_name, 'rt') as credentials_file:
            self.credentials = json.load(credentials_file)
        

    def connect(self):
        self.auth = tweepy.OAuthHandler(self.credentials['consumer_key'], 
                           self.credentials['consumer_secret'])

        self.auth.set_access_token(self.credentials['access_token'], 
                      self.credentials['access_token_secret'])
        
        self.api = tweepy.API(self.auth)

    
    def find_followers(self, search_id):
        self.search_id = search_id
        followers_list = self.api.followers_ids(search_id)
        return followers_list


class MyStreamListener(StreamListener):
    def __init__(self, api, mongo_db_name, mongo_coll_name, **kw):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.col = mongo.create_connection(mongo_db_name, **kw)[mongo_coll_name]


    def on_data(self, tweet):
        self.col.insert(json.loads(tweet))


    def on_error(self, status):
        return True # keeps stream open


## Testing the twitter reader ##
#TR = TwitterReader('twitter-credentials.json')
#TR.connect()
#followers = TR.find_followers('@SohrabKohli')
#print(followers)

## Testing Stream Listener ##
TR = TwitterReader('twitter-credentials.json')
TR.connect()
stream = tweepy.Stream(TR.auth, MyStreamListener(TR.api, 'tweets', 'tweets'))
stream.filter(track=['trump', 'javascript', 'dataviz'])
