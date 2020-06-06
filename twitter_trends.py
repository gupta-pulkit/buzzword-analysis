"""
Mention a topic, the code will get the tweets related to the topic.

Later:
Get the related words to the topic and get the tweets which have both.
"""
import pandas as pd
import tweepy
from tweepy import OAuthHandler, API, Stream
from tweepy.streaming import StreamListener
import json

class SListener(StreamListener):
    def __init__(self, api, max_tweets):
        self.api = api
        self.count = 0
        self.max_tweets = max_tweets
        self.output  = open('data/tweets.json', 'w')
        self.tweets = []

    def save(self):
        self.output.write(json.dumps(self.tweets))
        self.output.close()
        df = pd.DataFrame(self.tweets)
        df.to_csv('data/tweets.csv', index = False)

    def on_status(self, status):
        self.tweets.append(status._json)
        self.count += 1
        print("Getting tweet #{0}".format(self.count))
        if self.count == self.max_tweets:
            self.save()
            return False

        return True

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return

class TwitterBot:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        (self.auth, self.api) = self.get_api()

    def get_api(self):
        auth = OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = API(auth)

        return (auth, api)

    def fetch_data(self, keywords, max_tweets):
        listen = SListener(self.api, max_tweets = max_tweets)
        stream = Stream(self.auth, listen)
        stream.filter(track = keywords)

def main():
    with open('twitter_dev_config.json') as f:
        dev_config = json.load(f)

    api_key = dev_config['api_key']
    api_secret_key = dev_config['api_secret_key']
    access_token = dev_config['access_token']
    access_token_secret = dev_config['access_token_secret']

    bot = TwitterBot(api_key, api_secret_key, access_token, access_token_secret)
    bot.fetch_data(['covid', 'corona'], max_tweets = 1000)

if __name__=='__main__':
    main()
