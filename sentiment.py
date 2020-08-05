import tweepy
from textblob import TextBlob
import json
import argparse
import signal
import sys
from colorit import Colors, init_colorit, color

NEUTRAL_THRESHOLD = 0.1

avg = 0
count = 0
count_pos = 0
count_neg = 0

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--search-text", type=str, required=True)
    parser.add_argument("-a", "--auth-file", type=str, required=False, default="./auth.json")
    parser.add_argument("-t", "--enable-translation", action="store_true", help="To analyze non-english tweets you have to use this option")
    args = parser.parse_args()

    auth = read_json(args.auth_file)

    consumer_key = auth['consumer_key']
    consumer_secret = auth['consumer_secret']

    access_token = auth['access_token']
    access_token_secret = auth['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener(args.enable_translation)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=[args.search_text], is_async=True)
    
    init_colorit()


def analyze_polarity(text, enable_translation):
    blob = TextBlob(text)
    if enable_translation and blob.detect_language() != 'en':
        translation = TextBlob(str(blob.translate(to='en')))
        return translation.sentiment.polarity
    else:
        return blob.sentiment.polarity

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def display_info(ts, polarity, avg, count_pos, count_neg, count, text):
    print('{0}\t Polarity:{1}\tAvg:{2}\tPos:{3}\tNeg:{4}\tTot:{5}\t{6}'.format(ts, color_text(round(polarity,2)), color_text(round(avg,2)), count_pos, count_neg, count, text[:30] + '...'))

def color_text(val):
    if(val < -NEUTRAL_THRESHOLD):
        return color(val, Colors.red)
    if(val > NEUTRAL_THRESHOLD):
        return color(val, Colors.green)
    else:
        return color(val, Colors.yellow)


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, enable_translation):
        super(MyStreamListener, self).__init__()
        self.enable_translation = enable_translation

    def on_error(self, status_code):
        if status_code == 420:
            # returning non-False reconnects the stream, with backoff.
            return True

        #returning False in on_error disconnects the stream
        return False
            

    def on_status(self, tweet):

        global avg, count, count_pos, count_neg

        ts = tweet.created_at
        polarity = analyze_polarity(tweet.text, self.enable_translation)

        avg = (avg*count + polarity)/(count + 1)
        count = count + 1
        if polarity > 0:
            count_pos = count_pos + 1
        if polarity < 0:
            count_neg = count_neg + 1

        display_info(ts, polarity, avg, count_pos, count_neg, count, tweet.text)



def signal_handler(sig, frame):
    print('Bye!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()