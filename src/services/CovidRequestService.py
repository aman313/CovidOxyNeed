import logging

from src.models.Exceptions import ResponseNotSentException
from src.models.tweet import Tweet
import spacy
from spacy import displacy
from src.models.CovidRequest import CovidRequest
from src.services.CovidResourceService import CovidResourceService, TweetCovidResourceService
from src.services.RequestResourceMappingService import ResourceRequestMappingService
from src.services.ResponseService import ResponseCreationService, TwitterResponseSendingService


class CovidRequestService:
    pass

class TweetCovidRequestSevice(CovidRequestService):
    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")

    def get_requestFilter(self):
        return ['Request', 'Help', 'Need', 'Needed', 'SOS', 'Support', 'CovidSOS']

    def get_resourceTypeFilter(self):
        return TweetCovidResourceService().get_resourceTypeFilter()

    def handle_request(self, covid_request:CovidRequest):
        resource_request_mapping_service = ResourceRequestMappingService()
        mapped_resource = resource_request_mapping_service.map_request_to_resource(covid_request)
        response_sending_service = TwitterResponseSendingService()
        response_service = ResponseCreationService()
        if mapped_resource:
            response_message = response_service.form_response_message(covid_request,mapped_resource)
            try:
                response_sending_service.send_response_message(response_message)
            except ResponseNotSentException as e:
                logging.error('Could not respond to request ' + covid_request.request_url)
        else:
            logging.error('No response matched '+ covid_request.request_url)

    def extract_requested_resource_type(self, original, parsed):
        resource_type = self.get_resourceTypeFilter()
        for resource in resource_type:
            if resource.lower() in original.tweet_data.lower():
                return resource
        return ''

    def extract_request_location(self,original,parsed):
        for ent in parsed.ents:
            if ent.label_ == 'LOC':
                return ent.text
        return ''

    def is_request(self,original,parsed):
        if any([x.lower() in original.tweet_data.lower() for x in self.get_requestFilter()]):
            return True
        return False

    def parseTweetToRequest(self,tweet):
        doc = self._nlp(tweet.tweet_data)
        #displacy.render(doc, style="ent")
        location_name = self.extract_request_location(tweet,doc)
        resource_type = self.extract_requested_resource_type(tweet,doc)
        request_source = 'Twitter'
        is_request = self.is_request(tweet,doc)

        if is_request:
            covid_request = CovidRequest(request_source=request_source, request_location_name=location_name,
                                         requested_resource_type=resource_type, request_text=tweet.tweet_data,
                                         request_time=tweet.tweet_time, request_url=tweet.tweet_url)
            #print(covid_request.to_json())
            return covid_request