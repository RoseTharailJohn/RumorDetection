import numpy as np
import pandas as pd
#import nltk as nltk
#import cust_tokenizer as tk
import re
from dateutil.parser import parse as date_parse
import calendar
import matplotlib.pyplot as plt
import collections
from collections import defaultdict
from matplotlib import pylab

data_root = "C:/Users/anushree99/Desktop/RUMORS/Phase1-2015-11-15/Phase1"
timeTable=defaultdict(int)
countTable=[]
minT=0
maxT=0

def load_tweets_label(filepath) :
	#read the file
    df = pd.read_csv(filepath,sep='\t')
    #extract only the tweet and label for now
    columns_of_interest = ['date','tweet','label']
    df = df.reindex(columns=columns_of_interest)
    #we are interested in only if the tweet is a rumor or not - so,
    #we give it two classes - 0 - for not rumor, 1 - for rumor
    df.loc[df['label'] > 0, 'label'] = 1

    #df.loc[df['date']!='null', 'date'] = calendar.timegm((date_parse(df['date'])).timetuple())

    # for tw in df.iterrows():
    #     print tw[0]


    for i, trial in df.iterrows():
     df.loc[i, "date"] = calendar.timegm((date_parse(df.loc[i, "date"]).timetuple()))
     if (df.loc[i, "label"]==1):
         timeTable[df.loc[i, "date"]] = 1


    sorted(timeTable)
    #timeTable.sort()

    minT= min(timeTable.keys())
    maxT= max(timeTable.keys())

    # print timeTable

    i=minT
    width=1000000

    # print countTable
    return df

if __name__=='__main__':

    airfrance_raw = load_tweets_label(data_root+"/airfrance.txt")  #50k
    # palin_raw = load_tweets_label(data_root+"/palin.txt")  #50k
    # michelle_raw = load_tweets_label(data_root+"/michelle.txt")  #50k

    # print ("AF DATASET : ", airfrance_raw.shape)
    # print airfrance_raw.iloc[0]['label']
    # print airfrance_raw.iloc[1]['label']
    #print airfrance_raw.iloc[2]['date']

    # width=100
    # plt.hist(timeTable.keys(), timeTable.values(), width)

    minT= min(timeTable.keys())
    maxT= max(timeTable.keys())

    binNumbers= (maxT-minT)/50000

    newArray =  (np.asarray(timeTable.keys()))
    y,binEdges, patches = plt.hist(newArray,bins=binNumbers)
    plt.clf()
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

    plt.fill_between(bincenters,y, facecolor='green')
    plt.plot(bincenters,y, color= 'green')
    plt.ylabel("Number of tweets")
    plt.xlabel("Each passing hour")
    plt.show()



    # dt =  date_parse(airfrance_raw.iloc[2]['date'])
    # timestamp1 = calendar.timegm(dt.timetuple())

    # print timestamp1