import os
import tweepy
import sys
import requests

try:
    auth = tweepy.OAuthHandler(
        os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"],
                          os.environ["ACCESS_TOKEN_SECRET"])

    api = tweepy.API(auth)
except KeyError:
    print('No keys provided')
    # print('Missing the Twitter API keys. Quitting execution')
    # sys.exit()
    pass

regional_stats = requests.get('https://api.covid19tracker.ca/summary/split').json()

print('regional_stats', regional_stats['data'])
