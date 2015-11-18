import numpy as np
import pandas as pd
import nltk as nltk
import cust_tokenizer as tk
import re

data_root = "../Data/Phase1/"

def load_tweets_label(filepath) :
	#read the file
    df = pd.read_csv(filepath,sep='\t')
    #extract only the tweet and label for now
    columns_of_interest = ['tweet','label']
    df = df.reindex(columns=columns_of_interest)
    #we are interested in only if the tweet is a rumor or not - so, 
    #we give it two classes - 0 - for not rumor, 1 - for rumor
    df.loc[df['label'] > 0, 'label'] = 1
    return df

#feature extraction
#create empty array -- 7 columns - 1st 6 are features, 7th column is label
# col 0- count of question marks
# col 1- count of exclamation marks
# col 2- count of hashtags
# col 3- count of urls
# col 4- count of @ symbols
# col 5- count of question phrases
def extract_features(dataset) :
    num_of_tweets = dataset.shape[0]
    num_of_features = 7
    features = np.zeros((num_of_tweets, num_of_features))
    for i in range(0, num_of_tweets) :

        tweet = dataset.iloc[i]['tweet']
        label = dataset.iloc[i]['label']

        # set label column to tweets label
        features[i][6] = label

        # set other features after tokenizing and counting through all of them
        tweet_tokens = tk.preprocess(tweet)
        for token in tweet_tokens:
            # count num of question marks
            if token=='?' :
                features[i][0]+=1
            # count num of exclamation marks
            if token=='!' :
                features[i][1]+=1
            # count num of hashtags
            if re.search( r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", token) :
                features[i][2]+=1
            # count num of urls
            if re.search( r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', token) :
                features[i][3]+=1
            # count retweet
            if re.search( r'RT\s*(?:@[\w_]+)', token) :
                features[i][4]+=1
        # count question phrases
        tweet=tweet.lower()
        # question phrase - is(that | this | it ) true
        if(re.search( r"is\s+(that|this|it)\s+\w*\s*(real|rl|true)", tweet)):
           features[i][5]+=1
        # question phrase - omg, o my god, oh my god, oh my gawd
        if(re.search( r"(omg)|(o)(h)*\s*(my)\s*(god|gawd)", tweet)):
           features[i][5]+=1
        if(re.search( r"(are|is)\s*(true)", tweet ):
           features[i][5]+=1
        # question phrase - really? real etc..
        if(re.search( r"real(l|ll|lly|ly)*(\?|\!)+", tweet)):
           features[i][5]+=1
        # tweet contains the word unconfirmed or debunked
        if(re.search(r"(unconfirm)(ed)*", tweet)) :
           features[i][5]+=1
        if(re.search(r"(looks)\s*(like)", tweet)):
           features[i][5]+=1
        if(re.search(r"(debunk)(ed)*|(dismiss)(ed)*", tweet)):
           features[i][5]+=1
        # question phrase - what?? or something similar
        if(re.search(r"wh[a]*t[?!][?1]*", tweet)):
           features[i][5]+=1
        # question phrase - rumor?
        if(re.search(r"(rumor\s*)(\?)|(hoax)|(gossip)|(scandal)", tweet)):
           features[i][5]+=1
        # question phrase - truth or true
        if(re.search(r"(tru)(e|th)|(false)|(fake)", tweet)):
           features[i][5]+=1
        # question phrase - truth or true
        if(re.search(r"(den)(ial|y|ied|ies)|(plausible)", tweet)):
           features[i][5]+=1
        if(re.search(r"(plausible)", tweet)):
           features[i][5]+=1
        # question phrase - truth or true
        if(re.search(r"belie(f|ve|ving)", tweet)):
           features[i][5]+=1
        # question phrase - truth or true
        if(re.search(r"(why)|(what)|(wht)|(when)|(where)|(whr)", tweet)):
           features[i][5]+=1
    return features

if __name__=='__main__':

	## STEP 1 - LOAD DATA ##

	#load datafiles
	
	#we will use palin for training
	palin_raw = load_tweets_label(data_root+"palin.txt")
	
	#we will use airfrance and michelle for testing
	airfrance_raw = load_tweets_label(data_root+"airfrance.txt")
	michelle_raw = load_tweets_label(data_root+"michelle.txt")
	
	#join the two dataframes
	palin_boston_raw = palin_raw.append(boston_raw)
	michelle_airfrance_raw = michelle_raw.append(airfrance_raw)
	
	#stats of the dataset
	print ("PALIN DATASET : ", palin_boston_raw.shape)
	print ("MICHELLE - AIRFRANCE DATASET : ", michelle_airfrance_raw.shape)
	
	## STEP 2 - FEATURE EXTRACTION ##
	train_set = extract_features(palin_raw)
	test_set = extract_features(michelle_airfrance_raw)
	
	#print "before saving..."
	#print train_set[12]
	#print test_set[12]
	
	## STEP 3 - SAVE THE TRAINING AND TEST SET FILES ##
	np.save(data_root+"train.npy", train_set)
	np.save(data_root+"test.npy", test_set)
	
	#f1 = np.load(data_root+"train.npy")
	#f2 = np.load(data_root+"test.npy")
	#print "after saving..."
	#print f1[12]
	#print f2[12]
