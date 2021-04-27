import os
import tweepy
import sys
import requests

def get_population(province_stat):
    population = province_stat.get('population')
    return population if population else 0

try:
    auth = tweepy.OAuthHandler(
        os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"],
                          os.environ["ACCESS_TOKEN_SECRET"])

    api = tweepy.API(auth)
except KeyError:
    print('Missing the Twitter API keys. Quitting execution')
    sys.exit()

covid_stats = requests.get(
    'https://api.covid19tracker.ca/summary/split').json()['data']
region_stats = requests.get('https://api.covid19tracker.ca/provinces').json()
tweets = ['']
parent_tweet = None

region_stats.sort(key=get_population, reverse=True)

# Format the combined stats per tweet
for region in region_stats:
    covid_region_stats = next(
        (stat for stat in covid_stats if stat['province'] == region['code']), None)
    if covid_region_stats:
        current_tweet_count = len(tweets) - 1
        first_dose_count = covid_region_stats['total_vaccinations'] - \
            covid_region_stats['total_vaccinated']
        first_dose_percentage = f"{round(first_dose_count / region['population'] * 100, 1)}% (💉)"
        second_dose_percentage = f"{round(covid_region_stats['total_vaccinated'] / region['population'] * 100, 1)}% (💉💉)"

        province_tweet = f"{region['name']}: {first_dose_percentage} | {second_dose_percentage} | +{covid_region_stats['change_vaccinated']} administered today \n"
        combined_tweet = tweets[current_tweet_count] + province_tweet

        if len(combined_tweet) >= 273:
            tweets.append(province_tweet)
        else:
            tweets[current_tweet_count] = combined_tweet


# Add formating to each tweet and post it
for index, tweet in enumerate(tweets):
    formatted_tweet = f'({index + 1}/{len(tweets)}) ' + tweet

    print('Publishing tweet:' + formatted_tweet)
    if index == 0 or not parent_tweet:
        parent_tweet = api.update_status(status=formatted_tweet)
    else:
        api.update_status(status=formatted_tweet,
                          in_reply_to_status_id=parent_tweet.id, auto_populate_reply_metadata=True)
