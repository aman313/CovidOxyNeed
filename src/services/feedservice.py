import datetime
import json
import logging
import os
import urllib.parse
from typing import List
import tweepy

from src import constants
from src.constants import TwitterCredentials
from src.constants import TwitterCredentials, CommonConstants
from src.models.tweet import Tweet
from src.utilities import db_connection as db, db_insert_tweet_data
from src.services.CovidRequestService import CovidRequestService
from src.services.CovidResourceService import CovidResourceService

class FeedService:
    pass


class FilterCriterion:
    def __init__(self, content_filters: List[str] = None, hashtags: List[str] = None):
        self._content_filters = content_filters
        self._hastags = hashtags

    def get_query_string(self) -> str:
        query_string = ''
        conjunction_units = []

        if self._content_filters and len(self._content_filters):
            content_string = '( '
            for string in self._content_filters:
                if len(content_string)>2:
                    content_string+=' OR '+string
                else:
                    content_string += string
            content_string += ' )'
            conjunction_units.append(content_string)

        if self._hastags and len(self._hastags):
            hashtag_string = '( '
            for hahtag in self._hastags:
                if len(hashtag_string)>2:
                    hashtag_string+=' OR '+hahtag
                else:
                    hashtag_string += hahtag
            hashtag_string += ' )'
            conjunction_units.append(hashtag_string)

        for unit in conjunction_units:
            if unit:
                if len(query_string):
                    query_string = query_string + ' AND ' + unit
                else:
                    query_string = unit

        query_string = query_string + ' -filter:retweets'
        print(query_string)
        return urllib.parse.quote_plus(query_string)


class TwitterFeedService(FeedService):
    tweets = []

    def __init__(self, credentials: TwitterCredentials):
        auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def get_filters(self)->List[FilterCriterion]:
        covid_sos_criterion = FilterCriterion(hashtags=['covidSOS','CovidSOS','covidsos','covidSos'],content_filters=['oxygen'])
        return [covid_sos_criterion]

    def get_recent_tweets(self, duration_in_min: int = 5, count=20):

        since = datetime.datetime.utcnow() - datetime.timedelta(minutes=duration_in_min)

        for filter in self.get_filters():
            query_string = filter.get_query_string()
            try:
                for status in tweepy.Cursor(
                    self.api.search,
                    q=query_string,
                    count=count,
                    result='recent',
                    tweet_mode='extended',
                    include_entities=True
         ).items():
                    self.process_tweet(status)
                    if status.created_at < since:
                        break
                    # if status._json['full_text'].startswith('RT '):
                    #     continue
                    # with open(constants.dump_location+status._json['id_str'],'w') as o:
                    #     json.dump(status._json,o)

            except tweepy.TweepError as e:
                logging.error('Error fetching tweet')
                continue

        # self.insert_tweets()

    def process_tweet(self, status):
        tweet_id = status._json['id_str']
        tweet_data = status._json['full_text']
        tweet_time = status._json['created_at']
        tweet_url = CommonConstants.TWEET_URL + tweet_id
        tweet = Tweet(tweet_data=tweet_data, tweet_url=tweet_url, tweet_time=tweet_time)
        req_service = CovidRequestService(tweet)
        req_service.parseTweetToRequest()
        res_service = CovidResourceService(tweet)
        res_service.parseTweetToResource()

    def insert_tweets(self):
        db_insert_tweet_data.insert_tweet(self.tweets, self.connection)

    def stream(self):
        pass


if __name__ == '__main__':
    creds = TwitterCredentials()
    feed_service = TwitterFeedService(creds)
    feed_service.get_recent_tweets(duration_in_min=1)
