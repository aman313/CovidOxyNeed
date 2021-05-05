import logging

import spacy
from spacy import displacy
from src.models.CovidResource import CovidResource
from src.models.tweet import Tweet


class CovidResourceService:
    pass

class TweetCovidResourceService(CovidResourceService):
    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")

    def get_resourceFilter(self):
        return ['Available']

    def get_resourceTypeFilter(self):
        return ['Oxygen', 'Remdisivir', 'bed','plasma','oxygen concetrator','concentrator','baricitinib']

    def handle_resource(self, covid_resource:CovidResource):
        try:
            covid_resource.save()
            logging.warn('Saving resource: ' + covid_resource.to_json())
        except Exception as e:
            logging.error('Error while saving resource ' + covid_resource.to_json())

    def get_resources_by_type_and_location(self, resource_type, resource_location):
        valid_resources = CovidResource.objects(resource_type=resource_type,resource_location_name=resource_location)
        return valid_resources

    def extract_resource_type(self, original, parsed):
        resource_type = self.get_resourceTypeFilter()
        for resource in resource_type:
            if resource.lower() in original.tweet_data.lower():
                return resource
        return ''

    def extract_resource_location(self,original,parsed):
        for ent in parsed.ents:
            if ent.label == 'LOC':
                return ent.text
        return ''

    def is_resource(self,original,parsed):
        if any([x.lower() in original.tweet_data.lower() for x in self.get_resourceFilter()]):
            return True
        return False

    def parseTweetToResource(self,tweet:Tweet):
        doc = self._nlp(tweet.tweet_data)
        #displacy.render(doc, style="ent")
        location_name = self.extract_resource_location(tweet,doc)
        resource_type = self.extract_resource_type(tweet,doc)
        resource_source = 'Twitter'
        is_resource = self.is_resource(tweet,doc)

        if is_resource:
            covid_resource = CovidResource(resource_source=resource_source, resource_location_name=location_name,
                                           requested_resource_type=resource_type, resource_text=tweet.tweet_data,
                                           resource_time=tweet.tweet_time, resource_url=tweet.tweet_url)
            return covid_resource
