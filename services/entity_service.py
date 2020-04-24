from babel.dates import format_date
from dateparser import parse
from entities import CUSTOM_ENTITIES
from entities import PATH_DEFINITIONS
from utils import read_json


class EntityService(object):
    """ EntityService class """

    def __init__(self, lang):
        """ Initialize an EntityService isntance """
        self.lang = lang 
    
    @staticmethod
    def load_definition(label):
        """ Loads an Entity JSON file given its label """
        if label not in CUSTOM_ENTITIES:
            raise AttributeError("{} is not a custom entity".format(label))     

        file_path = '{}/{}.json'.format(PATH_DEFINITIONS, label)  
        data = read_json(file_path)
        return data
    
    def get_value(self, label, entry_id, text):
        """ Gets the value of an entry of a certain entity """
        if label == 'TIME':
            value = self._get_time_value(text)
        elif label == 'DATE': 
            value = self._get_date_value(text)
        else:
            value = self._get_default_value(label, entry_id, text)
        return value 

    def _get_default_value(self, label, entry_id, text):
        """ Gets the formatted string of an entity"""
        entries = EntityService.load_definition(label)['entries']
        entry = list(filter(lambda e: e['id'] == entry_id, entries))[0]
        value = entry['value'][self.lang]
        return value

    def _get_date_value(self, text):
        """ Gets the formatted string of a date """
        t_date = parse(text, languages=[self.lang]).date()
        return format_date(t_date, format='full', locale=self.lang)

    def _get_time_value(self, text):
        """ Gets the formatted string of a time """
        t_time = parse(text, languages=[self.lang]).time() 
        return t_time.isoformat(timespec='minutes')
