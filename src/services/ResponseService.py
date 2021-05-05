import logging

import tweepy
from tweepy import TweepError

from src import constants
from src.models.CovidRequest import CovidRequest
from src.models.CovidResource import CovidResource
from src.models.Exceptions import ResponseNotSentException
from src.models.Response import Response


class ResponseCreationService():

    def __init__(self):
        pass


    def form_response_message(self, covid_resource:CovidResource, covid_request: CovidRequest)->Response:
        response_text = covid_resource.resource_type + ' may have been available at ' + covid_resource.resource_time + '. For details check: ' + covid_resource.resource_url
        response = Response(original_request_id=covid_request.id,original_resource_id=covid_request.id,response_text=response_text)
        response.save()
        return response


class ResponseSendingService():

    def send_response_message(self, response:Response, original_request:CovidRequest):
        raise NotImplementedError

class TwitterResponseSendingService(ResponseSendingService):

    def __init__(self):
        credentials = constants.TwitterCredentials
        auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def send_response_message(self, response:Response, original_request:CovidRequest):
        original_tweet_id = original_request.request_url.split('/')[-1]
        try:
            logging.info('Sending response: \n')
            logging.info(original_request.to_json())
            logging.info(response.to_json())
            #self.api.update_status(status=response.response_text,in_reply_to_status_id=original_tweet_id,auto_populate_reply_metadata=True)
        except TweepError as e:
            logging.error('Unable to respond ' + str(e))
            raise ResponseNotSentException(e)
