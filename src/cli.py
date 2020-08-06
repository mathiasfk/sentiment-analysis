from twitter_sentiment_analysis import TwitterSentimentAnalysis
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

    TwitterSentimentAnalysis(auth, callback, args.search_text, args.enable_translation)
    
    init_colorit()


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def callback(tweet, sentiment):
    display_info(tweet.created_at, sentiment.polarity, sentiment.subjectivity, tweet.text)


def display_info(ts, polarity, subjectivity, text):
    print('{0}\t Polarity:{1}\tSubjectivity:{2}\t{3}'.format(ts, color_text(round(polarity,2)), color_text(round(subjectivity,2)), format_text(text)))


def format_text(text):
    return text[:80].replace('\n',' ') + '...'


def color_text(val):
    if(val < -NEUTRAL_THRESHOLD):
        return color(val, Colors.red)
    if(val > NEUTRAL_THRESHOLD):
        return color(val, Colors.green)
    else:
        return color(val, Colors.yellow)


def signal_handler(sig, frame):
    print('Bye!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()