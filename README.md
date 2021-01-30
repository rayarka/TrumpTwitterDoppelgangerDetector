# Is your twitter friend actually Donald Trump in disguise?

After twitter banned @therealdonaldtrump, the American president went on to tweet from different twitter accounts related to the Trump campaign. Apparently, his media manager - Gary Coby (@garycoby) - offered President trump his own account. Twitter noticed and swiftly banned @garycoby as well.

I believe that the Trump campaign will have learnt from that event. So now, if ex-President Trump wishes to use someone else's account secretly, they won't announce it, so that they can post undettered.

So who's to say that your new friend isn't actually <b>Donald Trump</b>?

<img src='https://user-images.githubusercontent.com/25000887/106347608-0d09ee00-62fb-11eb-9825-0496569e770b.png' height='250'>

## There's only 1 way to find out!

While he can change his profile details, we can assume that his tweets will remain somewhat similar! Humans are, after all, creatures of habit. So how can we figure out if your friend is secretly Donald Trump?

<i><b>Simple!</b></i>

We will see your friend's (or any public account's) recent tweets! And if they're similar to what DJT would have posted, I have some bad news for you :( We will be using the Levenshtein algorithm to compare your friends tweets to all of DJT's tweets over the past 6 months!

<b>Simply run the program (assuming you have Twitter's API keys) `python3 trumpdetection.py` and enter your suspect's username :)</b>

### Twitter Authentication
In my code, I've imported a custom module called `twitterauthentication.py`. In that module, I have listed out the Twitter API keys. You will need to get your own API keys to use this. You can learn how to do that <i>very easily</i> <a href='https://rapidapi.com/blog/how-to-use-the-twitter-api/'>here</a> (Note that this page also shows how to connect to the API. However, the code in `trumpdetection.py` already accounts for that through the use of the tweepy module). Alternatively, you can explore the twitter api and the tweepy module in greater depth with this <a href='https://www.youtube.com/watch?v=dvAurfBB6Jk'>great instructional video</a>

```
# The twitterauthentication.py file is written as below. 
# Listing the file under .gitignore ensures that you don't accidentally reveal your API keys if you push it online.

appAPIKey = "XXXXXXXXXXXXX"
appAPIKeySecret = "XXXXXXXXXXXXX"
appBearer = "XXXXXXXXXXXXX"
appAccess = "XXXXXXXXXXXXX"
appAccessSecret = "XXXXXXXXXXXXX"
```
