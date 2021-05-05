import os
from enum import Enum


class TwitterCredentials:
    API_KEY='NNVq017qyzQiSUsobeXuoA'
    API_SECRET='llYoDUUHN6kKGNdxidwHwiMrIeWVWmNI5DPFkx0AYo'
    ACCESS_TOKEN='52416153-4FX5fFVq7NZmftK3JsiPaSqUQup3mrTCPg4euMEfJ'
    ACCESS_TOKEN_SECRET='dzZ1iKXNFF74FiVzEJ0bKQmTU5UeInQoIBbrDDoUekVQf'

dump_location ='/media/aman/8a3ffbda-8a36-45f9-b426-d146a65d9ece/data1/open_source/oxy_need/tweet_dump/'

class CommonConstants:
    TWEET_URL = 'https://twitter.com/twitter/statuses/'
    DB_NAME = 'covid_resource_requests'


class ResourceTypes(Enum):
    OXYGEN = 1
    BED = 2
    REMDISIVIR = 3
    VENTILATOR = 4

class TweetTypes(Enum):
    COVID_RESOURCE_REQUEST = 1
    COVID_RESOURCE_SOURCE = 2
    OTHERS = 3