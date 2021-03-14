#!/usr/bin/env python3

#moody twit
#a twitter sentiment analysis script using NLP
#gavin su me@gavin.su
#2021

import sys
import tweepy
import json
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def loadKeys():
    '''
    Loads the keys located in the config.json file and returns them in a list.
    '''
    with open("config.json") as jsonFileRead:
        keys = json.load(jsonFileRead)
    keyList = [keys["ConsumerKey"],
            keys["ConsumerSecret"],
            keys["AccessToken"],
            keys["AccessTokenSecret"]]
    return keyList

def getTweets(api, keyword, count):
    '''
    Gets and returns an x amount of tweets based on the keyword provided.
    '''
    tweets = tweepy.Cursor(api.search, q=keyword).items(count)
    return tweets

def getSentiment(tweets):
    '''
    Returns a count of the positive, negative and neutral tweets in a list.
    '''
    positive = 0
    negative = 0
    neutral = 0
    #polarity = 0
    #tweetList = []
    for tweet in tweets:
        #tweetList.append(tweet.text)
        analysis = TextBlob(tweet.text)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        pos = score['pos']
        neg = score['neg']
        neu = score['neu']
        comp = score['compound']
        #polarity += analysis.sentiment.polarity
        if pos > neg:
            positive += 1
        elif neg > pos:
            negative += 1
        elif pos == neg:
            neutral += 1
    sentimentList = [positive,negative,neutral]

    return sentimentList

def moodytwit(keyword, count):
    keys = loadKeys()
    auth = tweepy.OAuthHandler(keys[0],keys[1])
    auth.set_access_token(keys[2],keys[3])
    api = tweepy.API(auth)
    tweets = getTweets(api, keyword, count)
    sentiment = getSentiment(tweets)
    return sentiment

def main():
    print(moodytwit(sys.argv[1], int(sys.argv[2])))
    return

if __name__=='__main__':
    main()
