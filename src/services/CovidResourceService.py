from src.models.tweet import Tweet
import spacy
from spacy import displacy
from src.models.CovidResource import CovidResource


class CovidResourceService:
    def __init__(self, tweet: Tweet):
        self.tweet = tweet

    def get_resourceFilter(self):
        return ['Available']

    def get_resourceTypeFilter(self):
        return ['Oxygen', 'Remdisivir', 'bed']

    def parseTweetToResource(self):
        nlp = spacy.load("xx_ent_wiki_sm")
        doc = nlp(self.tweet.tweet_data)
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

            if any(ent.text.lower() in s.lower() for s in self.get_resourceFilter()):
                is_request = True

        if is_request:
            covid_resource = CovidResource(request_source=request_source, request_location_name=location_name,
                                           requested_resource_type=resource_type, request_text=self.tweet.tweet_data,
                                           request_time=self.tweet.tweet_time, request_url=self.tweet.tweet_url)
            print(covid_resource)
            # TODO: Insert into collection


class TweetStreamCovidResourceService():
    pass
