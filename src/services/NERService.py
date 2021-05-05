from enum import Enum
from geograpy import Extractor

class EntityTypes(Enum):
    PLACE = 1
    HOSPITAL_NAME = 2
    MEDICINE_NAME = 3
    PHONE_NUMBER = 4


class NERService():

    def __init__(self):
        pass

    def extract_entities_from_text(self,text):
        raise NotImplementedError


class GeograpyPlaceExtractionService(NERService):
    __ent_type__ = EntityTypes.PLACE

    def __init__(self):
        pass

    def extract_entities_from_text(self,text):
        places = Extractor(text=text).find_geoEntities(text)
        if len(places):
            return places[0]
