import datetime
import logging

from src.constants import TweetTypes
from src.models.CovidResource import CovidResource
from src.models.CovidRequest import CovidRequest
from src.services.CovidResourceService import CovidResourceService, TweetCovidResourceService


class ResourceRequestMappingService():

    def __init__(self):
        self._resource_service = TweetCovidResourceService()
        self._recency_threshold_in_mins = 30

    def filter_resource_by_recency(self, resource:CovidResource):
        since = datetime.datetime.utcnow() - datetime.timedelta(minutes=self._recency_threshold_in_mins)
        resource_time = resource.resource_time
        if resource_time < since:
            return True
        return False

    def map_request_to_resource(self, covid_resource_request:CovidRequest)->CovidResource:
        request_resource_type = covid_resource_request.requested_resource_type
        request_location = covid_resource_request.request_location_name
        if request_location == '' or request_resource_type == '':
            return None
        valid_resources = self._resource_service.get_resources_by_type_and_location(request_resource_type,request_location)
        if len(valid_resources) > 0:
            logging.info('Filtered due to recency ' + covid_resource_request.to_json())
        recent_valid_resources = [x for x in filter(self.filter_resource_by_recency,valid_resources)]
        if len(recent_valid_resources):
            return recent_valid_resources[0]
