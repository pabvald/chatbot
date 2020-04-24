import numpy as np
from app import app, db
from intents import INTENTS, PATH_DEFINITIONS, INTENTS_PRIORITIES, FALLBACK_INTENT
from models import Intent, Parameter
from services.entity_service import EntityService
from services.knowledge_service import KnowledgeService
from utils import read_json

class IntentService(object):
    """IntentService class"""

    def __init__(self, lang, intent, responses, prompts, action):
        """ Initializes an IntentService instance """
        self.lang = lang
        self._intent = intent
        self._responses = responses
        self._prompts = prompts
        self._action = action
        self._entity_service = EntityService(self.lang)
        self._knowledge_service = KnowledgeService(self.lang)

    @staticmethod
    def priority(name):
        """ Determines the priority of an intent """
        return INTENTS_PRIORITIES.get(name, 0)

    @staticmethod
    def load_definition(name):
        """ Loads an Intent JSON file """
        if name not in INTENTS:
            raise AttributeError("'{}' is not a valid intent".format(name))
        file_path = '{}/{}.json'.format(PATH_DEFINITIONS, name)
        data = read_json(file_path)
        return data

    @classmethod
    def from_new_intent(cls, lang, name, user_id):
        """ Initializes an IntentService with a new intent """
        data = IntentService.load_definition(name)
        intent = Intent(name=name, user_id=user_id)
        prompts = dict(map(lambda par: (par['name'], par['prompts'][lang]), data['parameters']))
        for par in data['parameters']:
            intent.parameters.append(Parameter(par['name'], par['required'], par['entity']))
        return cls(lang, intent, data['responses'][lang], prompts, data.get('action', None))

    @classmethod
    def from_stored_intent(cls, lang, intent):
        """ Initializes an IntentService loading an existing intent """
        data = IntentService.load_definition(intent.name)
        prompts = dict(map(lambda par: (par['name'], par['prompts'][lang]), data['parameters']))
        return cls(lang, intent, data['responses'][lang], prompts, data.get('action', None))

    def get_response(self, doc):
        """ Generates a message response considering the intent's 
            name """
        if self._intent.name == FALLBACK_INTENT:
            response = self._generate_response_fallback(doc)
        else:
            response = self._generate_response_default(doc)
        return response

    def get_action(self):
        """ Obtains the intent's associated action. If the intent has 
            no action or it's not completed, None is returned """
        return self._action if self._intent.completed else None

    def get_params(self):
        """ Gets the intent parameters as a dictionary of (name, value)
            pairs """
        params_values = dict(map(lambda param: (param.name, param.value), self._intent.obtained_parameters))
        return params_values

    def reset_params(self, **params):
        """ Deletes the obtained values of the given params in order to 
            obtain them again """
        for name in params.keys():
            for parameter in self._intent.parameters:
                if parameter.name == name:
                    parameter.original = None
                    parameter.value = None

    def save_intent(self):
        """ Stores the intent in the database if it is not completed. Removes it 
            from the database if it is already completed """
        try:
            if self._intent.completed and self._intent.stored:
                db.session.delete(self._intent)
            if not self._intent.completed and not self._intent.stored:
                db.session.add(self._intent)
            db.session.commit()
        except Exception as e:
            app.logger.error(str(e))
            raise

    def _ask_for_param(self):
        """ Obtains a propmt message to ask for a parameter. Selects
            a msg randomly among those available """
        p = self._prompts[self._intent.required_parameters[0].name]
        rand = np.random.randint(0, len(p))
        return p[rand]

    def _final_response(self):
        """ Obtains a the final msg response of an intent. Selects a
            msg randomly among those available """
        rand = np.random.randint(0, len(self._responses))
        return self._responses[rand]

    def _generate_response_fallback(self, doc):
        """ Checks the Knowledge base before provinding a fallback response """
        knowledge_query = self._knowledge_service.get_response(doc)
        if knowledge_query:
            response = knowledge_query
        else:
            response = self._final_response()
        return response

    def _generate_response_default(self, doc):
        """ Generates a message response """
        # Extract parameters values    
        matched_entities = list(filter(lambda e: e.label_ in
                                                 list(map(lambda p: p.entity, self._intent.parameters)),
                                       doc.ents))
        if matched_entities:
            for par in self._intent.parameters:
                for ent in matched_entities:
                    if par.entity == ent.label_:
                        par.original = ent.text
                        par.value = self._entity_service.get_value(ent.label_, ent.ent_id_, ent.text)
        # Get the appropiate response
        if not self._intent.completed:
            response = self._ask_for_param()
        else:
            response = self._final_response()

        return response.format(**self.get_params())
