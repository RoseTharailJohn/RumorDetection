import oauth2 as oauth
import urllib2 as urllib
import sys
import json
import pandas as pd
from collections import defaultdict

api_key = "gHRSRSn6oN2Vfw5OzyKNUI5fK"
api_secret = "GEJIk7O1mGVq6wRTOHDSXKFoK5i75LibPph51N73WxHqQ6wOoH"
access_token_key = "155203347-KHhbqxgBHVwXUtkHssrkPKq4JN99c77KgS3A07qS"
access_token_secret = "bk9aq3q2Uak0Wf0SJJ7t1a6ee3NoiNeTL8Esaib3k7lDn"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


data_root = "C:/Users/anushree99/Desktop/RUMORS/Phase1-2015-11-15/Phase1"
timeTable=defaultdict(int)
countTable=[]
minT=0
maxT=0

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples(name):

  # url = "https://stream.twitter.com/1/statuses/sample.json"
  url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=440"%name

  # url ="https://api.twitter.com/1.1/search/tweets.json?q=%s&count=4000&rpp=4000"%name

  # id=839589814
  # url = "https://api.twitter.com/1.1/statuses/show.json?id=%s"%id
  #?screen_name=anushree99&count=2"

  parameters=[]
  response = json.load(twitterreq(url, "GET", parameters))

  print response

  # print response["text"]
  # print response["created_at"]

  # texts = [(tweet["text"]).encode("utf-8") for tweet in response["statuses"]]

  # texts = [(tweet["text"]).encode("utf-8") for tweet in response]

  # for line in response:
    # print line.strip()

  # print texts
  # file = open("brendon.txt", "w")
  # with open("test.txt", "a") as myfile:
  #
  #     for t in texts:
  #         text=t.replace('\n','')
  #         text=text.replace('\t','')
  #
  #         myfile.write(text+"\t0\n")
  #
  #
  # myfile.close()

  # statuses = response.json()
  # print "\n".join([status["text"] for status in statuses])

def load_tweets_label(filepath) :
	#read the file
    # df = pd.read_csv(filepath,sep='\t')
    #extract only the tweet and label for now
    # columns_of_interest = ['date','tweet','label']
    # df = df.reindex(columns=columns_of_interest)
    #we are interested in only if the tweet is a rumor or not - so,
    #we give it two classes - 0 - for not rumor, 1 - for rumor
    # df.loc[df['label'] > 0, 'label'] = 1

    idFile = open(filepath, "r")
    file = open("obama-with-Text.txt", "w")

    # file.write("hello world in the new file\n")
  #?screen_name=anushree99&count=2"

    parameters=[]


    for line in idFile:
        # text = fetchsamples(df.loc[id, 'tweetId'])

        id=line.split("\t")[0]
        label=line.split("\t")[1]
        url = "https://api.twitter.com/1.1/statuses/show.json?id=%s"%id
        response = json.load(twitterreq(url, "GET", parameters))

        try:
            text = response["text"]
            date = response["created_at"]
            file.write(date + "\t" + text  + "\t" +  label)

        except:
            print "error"

    file.close()




if __name__ == '__main__':
  # print sys.argv[1]
  fetchsamples("brendan642")
  #       load_tweets_label(data_root+"/obama-ids.txt")  #50k

