import logging

import spacy
from spacy import displacy
from src.models.CovidResource import CovidResource
from src.models.tweet import Tweet


class CovidResourceService:
    pass

class TweetCovidResourceService(CovidResourceService):
    def __init__(self):
        pass

    def get_resourceFilter(self):
        return ['Available']

    def get_resourceTypeFilter(self):
        return ['Oxygen', 'Remdisivir', 'bed']

    def handle_resource(self, covid_resource:CovidResource):
        try:
            covid_resource.save()
        except Exception as e:
            logging.error('Error while saving resource ', covid_resource.to_json())

    def get_resources_by_type_and_location(self, resource_type, resource_location):
        valid_resources = CovidResource.objects(resource_type=resource_type,resource_location_name=resource_location)
        return valid_resources

    def parseTweetToResource(self,tweet:Tweet):
        nlp = spacy.load("xx_ent_wiki_sm")
        doc = nlp(tweet.tweet_data)
        displacy.render(doc, style="ent")
        location_name = ''
        resource_type = ''
        request_source = 'Twitter'
        location_found = False
        is_resource = False
        for ent in doc.ents:
            if ent.label_ == 'LOC':
                if location_found is False:
                    location_name = ent.text
                    location_found = True

            if any(ent.text.lower() in s.lower() for s in self.get_resourceTypeFilter()):
                resource_type = ent.text

            if any(s.lower() in tweet.tweet_data.lower()  for s in self.get_resourceFilter()):
                is_resource = True

        if is_resource:
            covid_resource = CovidResource(resource_source=request_source, resource_location_name=location_name,
                                           requested_resource_type=resource_type, resource_text=tweet.tweet_data,
                                           resource_time=tweet.tweet_time, resource_url=tweet.tweet_url)
            return covid_resource
