import csv
from enum import Enum

from fuzzyset import FuzzySet
from geograpy import Extractor
import stanza
from spacy.lang.en import English

from src.constants import CommonConstants


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


class StanzaPlaceExtractionService(NERService):
    __ent_type__ = EntityTypes.PLACE

    def __init__(self):
        self.nlp = stanza.Pipeline(lang='en',processors='tokenize,ner',use_gpu=False)

    def extract_entities_from_text(self,text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent._type == 'GPE':
                return ent._text


class ListBasedPlaceExtractionService(NERService):

    def __init__(self, dist_file=CommonConstants.INDIA_DIST_NAMES):
        super().__init__()
        self.old_names = {'bangalore':'bengaluru','gurgaon':'gurugram','calcutta':'kolkata','prayagraj':'allahabad','delhi':'delhi'}
        self.fd = FuzzySet()
        self.set = set()
        with open(dist_file) as df:
            reader = csv.reader(df)
            header = next(reader)
            for row in reader:
                if 'rural' in row[1].lower() or 'urban' in   row[1].lower() or 'dehat' in  row[1].lower():
                    alternate = ' '.join(row[1].split(' ')[:-1]).lower()
                    self.fd.add(alternate)
                    self.set.add(alternate)
                    continue
                self.fd.add(row[1].lower())
                self.set.add(row[1].lower())
        self.nlp = stanza.Pipeline(lang='en',processors='tokenize',use_gpu=False)

    def extract_entities_from_text(self,text):
        doc = self.nlp(text)
        closest_match = (0,None)
        '''
        for token in doc.ents:
            tok_text = token.text.lower()
            closest_dist = self.fd.get(tok_text)
            if closest_dist and len(closest_dist):
                closest = closest_dist[0]
                if closest[0] > closest_match[0]:
                    closest_match = closest
        if closest_match[0] > 0.5:
            return closest_match[1]
        '''
        for sent in doc.sentences:
            for token in sent.tokens:
                tok_text = token.text.lower()
                if tok_text in self.set:
                    return tok_text
                try:
                    return self.old_names[tok_text]
                except KeyError:
                    continue