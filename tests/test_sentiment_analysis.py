from mockito import when, mock, verify
import unittest
from src.twitter_sentiment_analysis import analyze_sentiment

class TwitterSentimentAnalysisTest(unittest.TestCase):

  def test_analyze_sentiment_pos(self):
    negative_sentiment = analyze_sentiment("I really hate unit tests!!")
    self.assertLess(negative_sentiment.polarity, 0)

  def test_analyze_sentiment_neg(self):
    positive_sentiment = analyze_sentiment("I love unit tests!")
    self.assertGreater(positive_sentiment.polarity, 0)

if __name__ == '__main__':
    unittest.main()