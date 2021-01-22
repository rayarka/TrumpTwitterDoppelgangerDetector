import pandas as pd
from fuzzywuzzy import fuzz
import tweepy
import webbrowser
import time
from twitterauthentication import appAPIKey, appAPIKeySecret

#LOGGING
start = time.time()

#Authentication Details
consumer_key = appAPIKey    #Get from Twitter
consumer_secret = appAPIKeySecret   #Get from Twitter
callback_uri = 'oob'    #Unsure about how to implement but apparently if you're not doing this on some website, you can use 'oob' to handle it

trump_csv = "mid20to2021_trump_tweets.csv"  #Reference to file where trump tweets are stored
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
    for tweet in tweepy.Cursor(api.user_timeline,id=username).items(max_tweets):
        user_corpus.append(tweet.text.split("https")[0])
    return user_corpus

def trump_data_parsing(csvfile):
    print("Hmm highly odd...")
    trump_fulltweetdata = pd.read_csv(csvfile)
    trump_corpus = trump_fulltweetdata['text'].str.split("https", expand=True)
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
                print("Processing...")
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
    return None

api = authentication(consumer_key, consumer_secret, callback_uri)
username = input("Enter the username you suspect of being Donald Trump (public profiles only): @")
user_corpus = user_data_parsing(api, username, max_tweets)
trump_corpus = trump_data_parsing(trump_csv)
similarity_scores = data_comparison(user_corpus, trump_corpus)
user_similarity_verdict(username, similarity_scores, percentage_confidence=70)

print(f"\nThis operation took {time.time()-start:.0f} seconds")