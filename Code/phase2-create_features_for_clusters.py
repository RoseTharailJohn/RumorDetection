from __future__ import division
import numpy as np
import pandas as pd
import nltk as nltk
import matplotlib as plt
import re
from scipy.stats import entropy
from collections import defaultdict

data_root = "../Data/Phase2/"
regex_str = [
    r'<[^>]+>', # HTML tags
    r'RT\s*(?:@[\w_]+)', #RT @-Retweets
    r'(?:@[\w_]+)', #@-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if tokens_re.search(token) else token.lower() for token in tokens]
    return tokens

def is_signal_tweet(tweet) :
    # count question phrases
    # question phrase - is(that | this | it ) true
    tweet=tweet.lower()
    # question phrase - is(that | this | it ) true
    if(re.search( r"is\s+(that|this|it)\s+\w*\s*(real|rl|true)", tweet)):
        return True
    # question phrase - omg, o my god, oh my god, oh my gawd
    if(re.search( r"(omg)|(o)(h)*\s*(my)\s*(god|gawd)", tweet)):
        return True
    if(re.search( r"(are|is)\s*(true)", tweet )):
        return True
    # question phrase - really? real etc..
    if(re.search( r"real(l|ll|lly|ly)*(\?|\!)+", tweet)):
       return True
    # question phrase - what?? or something similar
    if(re.search(r"wh[a]*t[?!][?1]*", tweet)):
       return True
    # question phrase - rumor?
    if(re.search(r"(rumor\s*)(\?)|(hoax)|(gossip)|(scandal)", tweet)):
       return True
    # tweet contains the word unconfirmed or debunked
    if(re.search(r"(unconfirm)(ed)*", tweet)) :
       return True
    if(re.search(r"(debunk)(ed)*|(dismiss)(ed)*", tweet)):
       return True
    # question phrase - truth or true
    if(re.search(r"(tru)(e|th)|(false)|(fake)", tweet)):
       return True
    # question phrase - truth or true
    if(re.search(r"(den)(ial|y|ied|ies)|(plausible)", tweet)):
       return True
    return False

def partition_to_signal_and_ordinary(tweets_in_cluster):
    signal_tweets = []
    ordinary_tweets = []
    for tweet in tweets_in_cluster:
        if(is_signal_tweet(tweet)):
           signal_tweets.append(tweet)
        else :
            ordinary_tweets.append(tweet)
    return (signal_tweets,ordinary_tweets)

def get_token_list(tweets_list):
    token_list = []
    for tweet in tweets_list:
        token_list.append(preprocess(tweet))
    return token_list

def entropy_tweet(words_list):
    words_len=len(words_list)
    counts=defaultdict(float)
    for w in words_list:
        counts[w] +=1 #increment count of w word
    for w in counts.keys():
        counts[w] = float(counts[w]/words_len)#increment count of w word
    word_freqDist=list(counts.values())
    return entropy(word_freqDist)

def entropy_ratio(signal_words_list,all_words_list):
    return entropy_tweet(signal_words_list)/entropy_tweet(all_words_list)

def get_avg_tweet_len(tweets_list):
    token_count=0
    for tweet in tweets_list:
        tokens = preprocess(tweet)
        token_count+=len(tokens)
    return (token_count/len(tweets_list))

#percentage of retweets in the tweet list
def get_percentage_of_retweets(tweets_list):
    retweets_count = 0
    for tweet in tweets_list:
        # count retweet
        if re.search( r'RT\s*(?:@[\w_]+)', tweet) :
            retweets_count+=1
    return (retweets_count/len(tweets_list))

def get_avg_url_count(tweets_list):
    url_count=0
    for tweet in tweets_list:
        tokens = preprocess(tweet)
        for token in tokens:
            # count num of urls
            if re.match( r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', token) :
                url_count+=1
    return (url_count/len(tweets_list))

def get_avg_hashtag_count(tweets_list):
    hashtag_count=0
    for tweet in tweets_list:
        tokens = preprocess(tweet)
        for token in tokens:
            # count num of urls
            if re.match( r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", token) :
                hashtag_count+=1
    return (hashtag_count/len(tweets_list))

def get_avg_mention_count(tweets_list):
    mention_count=0
    for tweet in tweets_list:
        tokens = preprocess(tweet)
        for token in tokens:
            # count num of urls
            if re.match( r"(?:@[\w_]+)", token) :
                print token
                mention_count+=1
    return (mention_count/len(tweets_list))

# features description - this is for every cluster
# 0 - percentage of signal tweets
# 1 - entropy ratio
# 2 - tweet length - avg num of words per signal tweet
# 3 - tweet length - avg num of words per any tweet
# 4 - ratio of 3:4
# 5 - retweets - percentage of retweets among signal tweets
# 6 - retweets - percentage of retweets among all tweets
# 7 - urls - average num of URLs per signal tweet
# 8 - urls - average num of URLS per any tweet
# 9 - hashtags - average num of hashtags per signal tweet
# 10 - hashtags - average num of hashtags per tweet in cluster
# 11 - @mentions - average num of @mentions per signal tweet
# 12 - @mentions - average num of @mentions per tweet in cluster

def get_features_for_clusters(cluster_tweets_dict) :
    features = np.zeros((len(cluster_tweets_dict.keys()), 13))
    i=0
    for cluster_id in cluster_tweets_dict.keys():
        tweets_in_cluster = cluster_tweets_dict[cluster_id]
        (signal_tweets, ordinary_tweets) = partition_to_signal_and_ordinary(tweets_in_cluster)
        features[i][0] = len(signal_tweets)/len(tweets_in_cluster)
        features[i][1] = entropy_ratio(get_token_list(signal_tweets), get_token_list(tweets_in_cluster))
        features[i][2] = get_avg_tweet_len(signal_tweets)
        features[i][3] = get_avg_tweet_len(tweets_in_cluster)
        features[i][4] = features[i][2] / features[i][3]
        features[i][5] = get_percentage_of_retweets(signal_tweets)
        features[i][6] = get_percentage_of_retweets(tweets_in_cluster)
        features[i][7] = get_avg_url_count(signal_tweets)
        features[i][8] = get_avg_url_count(tweets_in_cluster)
        features[i][9] = get_avg_hashtag_count(signal_tweets)
        features[i][10] = get_avg_hashtag_count(tweets_in_cluster)
        features[i][11] = get_avg_mention_count(signal_tweets)
        features[i][12] = get_avg_mention_count(tweets_in_cluster)
        i+=1
    return features

if __name__=='__main__':
    # fill this later with the right data
    cluster_tweets_dict=defaultdict()
    np.save(data_root+"train.npy", get_features_for_clusters(cluster_tweets_dict))