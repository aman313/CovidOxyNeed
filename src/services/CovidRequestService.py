import logging

from src.models.Exceptions import ResponseNotSentException
from src.models.tweet import Tweet
import spacy
from spacy import displacy
from src.models.CovidRequest import CovidRequest
from src.services.RequestResourceMappingService import ResourceRequestMappingService
from src.services.ResponseService import ResponseCreationService, TwitterResponseSendingService


class CovidRequestService:
    pass

class TweetCovidRequestSevice(CovidRequestService):
    def __init__(self):
        pass

    def get_requestFilter(self):
        return ['Request', 'Help', 'Need', 'Needed', 'SOS', 'Support', 'CovidSOS']

    def get_resourceTypeFilter(self):
        return ['Oxygen', 'Remdisivir', 'bed']

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
            logging.info('No response matched '+ covid_request.request_url)

    def parseTweetToRequest(self,tweet):
        nlp = spacy.load("xx_ent_wiki_sm")
        doc = nlp(tweet.tweet_data)
        displacy.render(doc, style="ent")
        location_name = ''
        resource_type = ''
        request_source = 'Twitter'
        location_found = False
        is_request = False
        for ent in doc.ents:
            if ent.label_ == 'LOC':
                if location_found is False:
                    location_name = ent.text
                    location_found = True

            if any(ent.text.lower() in s.lower() for s in self.get_resourceTypeFilter()):
                resource_type = ent.text

            if any(ent.text.lower() in s.lower() for s in self.get_requestFilter()):
                is_request = True

        if is_request:
            covid_request = CovidRequest(request_source=request_source, request_location_name=location_name,
                                         requested_resource_type=resource_type, request_text=tweet.tweet_data,
                                         request_time=tweet.tweet_time, request_url=tweet.tweet_url)
            #print(covid_request.to_json())
            return covid_request