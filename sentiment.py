import tweepy
from textblob import TextBlob
import json
import argparse

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
    avg = 0
    count = 0
    count_pos = 0
    count_neg = 0

    while(True):
        tweets = api.search(args.search_text)
        for tweet in tweets:
            ts = tweet.created_at
            polarity = analyze_polarity(tweet.text, args.enable_translation)

            avg = (avg*count + polarity)/(count + 1)
            count = count + 1
            if polarity > 0:
                count_pos = count_pos + 1
            if polarity < 0:
                count_neg = count_neg + 1

            display_info(ts, polarity, avg, count_pos, count_neg, count)


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

def display_info(ts, polarity, avg, count_pos, count_neg, count):
    print('{0}\t Polarity:{1}\tAvg: {2}\tPos:{3}\tNeg:{4}\tTot:{5}'.format(ts, polarity, avg, count_pos, count_neg, count))

if __name__ == "__main__":
    main()