import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import tweepy
import webbrowser
import time
import random
from twitterauthentication import appAPIKey, appAPIKeySecret
import sys

#DEBUG MODE?
gettrace = getattr(sys,'gettrace',None) #Checking to see if we're in debug mode. This is mainly for my purposes cause I can't seem to debug when I'm in a nested folder inside a virtual environment.
if gettrace() is None: #Regular (non-debug) mode
    trump_csv = "mid20to2021_trump_tweets.csv"  #Reference to file where trump tweets are stored
elif gettrace():    #In Debug Mode (This next line is specific to the way I've set up my directories)
    trump_csv = "TrumpTwitterDoppelgangerDetector\\mid20to2021_trump_tweets.csv" #Reference to file where trump tweets are stored (nested)
else:
    print("How'd we end up here?")
    print(1/0)

#Authentication Details
consumer_key = appAPIKey    #Get from Twitter
consumer_secret = appAPIKeySecret   #Get from Twitter
callback_uri = 'oob'    #Unsure about how to implement but apparently if you're not doing this on some website, you can use 'oob' to handle it

max_tweets = 30 #Number of tweets from user-provided account to analyse. Given that the trump tweet dataset has 1984 values, each extra tweet means that the string similarity algorithm runs 1984 times more.

def authentication(consumer_key, consumer_secret, callback_uri):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
    try:
        api = tweepy.API(auth)
        # sname = api.me().screen_name
        print('API already ready')
        return api
    except:
        redirect_url = auth.get_authorization_url()
        webbrowser.open(redirect_url)
        user_pin_input = input("What's the pin value? ")
        auth.get_access_token(user_pin_input)
        api = tweepy.API(auth)
        # sname = api.me().screen_name
        print('API prepared and ready to use')
        return api

def user_data_parsing(api, username, max_tweets):
    print("Hmm... seems suspicious. Let me check it out!")
    user_corpus = []
    try:
        for tweet in tweepy.Cursor(api.user_timeline,id=username).items(max_tweets):
            user_corpus.append(tweet.text.split("https")[0])
    except:
        print(f"The '{username}' account is either private or invalid. Please check.")
        exit(1)
    return user_corpus

def trump_data_parsing(csvfile):
    print("Hmm highly odd...")
    trump_fulltweetdata = pd.read_csv(csvfile)
    trump_corpus = trump_fulltweetdata['text'].str.split("http", expand=True)
    trump_corpus = trump_corpus[0]
    return trump_corpus

def data_comparison(user_corpus, trump_corpus):
    list_of_scores = []
    for i in trump_corpus:
        for j in user_corpus:
            list_of_scores.append(
                {
                    'ratio': fuzz.WRatio(i, j),
                    'TrumpText': i,
                    'UserText': j
                }
            )
            if len(list_of_scores)%10000 == 0:
                print(random.choice(["Processing...","COVFEFE","CHINA!","Mexico will pay for the wall!","Fake News!"]))
    return list_of_scores

def user_similarity_verdict(username, scores, percentage_confidence):
    ldf = pd.DataFrame(scores)
    ldf = ldf.sort_values(by="ratio", ascending=False)
    number_above_confidence = ldf[ldf['ratio']>=percentage_confidence].shape[0]
    total_number = ldf.shape[0]
    percent_similar = 100*number_above_confidence/total_number
    print("HERE ARE MY FINDINGS:\n--------------------")
    time.sleep(2)
    print(f'{number_above_confidence} out of {total_number} tweets are at or above {percentage_confidence}% similarity.')
    print(f'Hence, @{username} is {percent_similar:.0f}% similar to @therealdonaldtrump!\nIn my expert opinion...')
    time.sleep(2)
    if percent_similar>50:
        print("This person is Donald Trump! Confront them with the truth!")
    elif percent_similar>20:
        print("This person may be Donald Trump! Keep an eye on them :|")
    else:
        print("This person is probably not the Donald... for now...")
    return ldf

api = authentication(consumer_key, consumer_secret, callback_uri)
username = input("Enter the username you suspect of being Donald Trump (public profiles only): @")

start = time.time() #LOGGING - Implemented here so that 

user_corpus = user_data_parsing(api, username, max_tweets)
trump_corpus = trump_data_parsing(trump_csv)
similarity_scores = data_comparison(user_corpus, trump_corpus)
df = user_similarity_verdict(username, similarity_scores, percentage_confidence=50)

end_of_main = time.time()

# # Below code is for sanity checking. It shows that this algorithm is not ideal for this application. 
# print(f"You most similar tweet was:\n{username}: {df['UserText'][0]}\nDonald Trump: {df['TrumpText'][0]}")

#plots
plt.hist(df['ratio'])
plt.title(f"How similar are Donald Trump and {username}'s tweets?", fontsize=12)
plt.xlabel("Percentage Similarity (%)", fontsize=10)
plt.ylabel("Similar Tweet Pairs", fontsize = 10)
end_of_plotting = time.time()
plt.show()

print(f"\nThe main operation took {end_of_main-start:.0f} seconds")