# Basic Sentiment Analysis

## Requisites

* Python 3
* pip

## Installation

```
pip install textblob
pip install tweepy
python -m textblob.download_corpora
```

Get your Tweeter API in https://developer.twitter.com/en.

Save a file named `auth.json` with your tokens. An example is provided in `auth.sample.json`.

## Running 

```
python src/cli.py -s "Donald Trump"
```

By default it only works with english tweets. To enable translation, use `-t`:

```
python src/cli.py -s "Jair Bolsonaro" -t 
```

Note that both Google Translate API and Twitter API have request rate limits, so the program might not work after passing that limit.