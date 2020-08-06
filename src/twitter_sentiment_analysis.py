import tweepy
from textblob import TextBlob
import json
import argparse
import signal

NEUTRAL_THRESHOLD = 0.1


class TwitterSentimentAnalysis:

    def __init__(self, auth, callback, search_text, enable_translation=False):

        consumer_key = auth['consumer_key']
        consumer_secret = auth['consumer_secret']

        access_token = auth['access_token']
        access_token_secret = auth['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token,access_token_secret)

        api = tweepy.API(auth)

        stream_listener = MyStreamListener(callback, enable_translation)
        stream = tweepy.Stream(auth = api.auth, listener=stream_listener)
        stream.filter(track=[search_text], is_async=True)


def analyze_sentiment(text, enable_translation):
    blob = TextBlob(text)
    if enable_translation and blob.detect_language() != 'en':
        translation = TextBlob(str(blob.translate(to='en')))
        return translation.sentiment
    else:
        return blob.sentiment


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, callback, enable_translation):
        super(MyStreamListener, self).__init__()
        self.callback = callback
        self.enable_translation = enable_translation

    def on_error(self, status_code):
        if status_code == 420:
            # returning non-False reconnects the stream, with backoff.
            return True

        #returning False in on_error disconnects the stream
        return False
            

    def on_status(self, tweet):
        sentiment = analyze_sentiment(tweet.text, self.enable_translation)
        self.callback(tweet, sentiment)