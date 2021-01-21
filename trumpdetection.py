import pandas as pd
from fuzzywuzzy import fuzz
import tweepy
import webbrowser
import time
from twitterauthentication import appAPIKey, appAPIKeySecret

start = time.time()
consumer_key = appAPIKey
consumer_secret = appAPIKeySecret
callback_uri = 'oob'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)

try:
    api = tweepy.API(auth)
    # sname = api.me().screen_name
    print('API already ready')
except:
    redirect_url = auth.get_authorization_url()
    webbrowser.open(redirect_url)
    user_pin_input = input("What's the pin value? ")
    auth.get_access_token(user_pin_input)
    api = tweepy.API(auth)
    # sname = api.me().screen_name
    print('API prepared')

# me = api.me()
# print(me.screen_name)

username = input("Enter the username you suspect of being Donald Trump (public profiles only): @")
max_tweets = 30
user_corpus = []
for tweet in tweepy.Cursor(api.user_timeline,id=username).items(max_tweets):
    user_corpus.append(tweet.text.split("https")[0])

trump_fulltweetdata = pd.read_csv("mid20to2021_trump_tweets.csv")
# print(trump_fulltweetdata['text'][2])

trump_corpus = trump_fulltweetdata['text'].str.split("https", expand=True)
trump_corpus = trump_corpus[0]
# print(trump_corpus[0])

# for val in trump_corpus:
#     print(val)
# print(type(trump_corpus[0]))
# try:
#     trump_corpus.dropna(inplace=True)
# except:
#     pass

l = []
for i in trump_corpus:
    for j in user_corpus:
        l.append(
            {
                'ratio': fuzz.WRatio(i, j),
                'TrumpText': i,
                'UserText': j
            }
        )

percentconf = 90
ldf = pd.DataFrame(l)
ldf_sorted = ldf.sort_values(by="ratio", ascending=False)
print(ldf_sorted.head())
print(ldf_sorted[ldf_sorted['ratio']>=percentconf].shape[0], "out of", ldf_sorted.shape[0], f"above {percentconf}% similar")

print(f"\nIt took {time.time()-start:.0f} seconds")