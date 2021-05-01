from time import sleep

from src.constants import TwitterCredentials
from src.services.feedservice import TwitterFeedService


def get_oxy_tweets():
    creds = TwitterCredentials()
    tweet_service = TwitterFeedService(creds)
    while(1):
        tweet_service.get_recent_tweets(duration_in_min=1)
        sleep(60)


get_oxy_tweets()