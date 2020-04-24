from app import app, nlp
from brain import ACTIONS, LANGUAGES
from dateparser import parse
from datetime import datetime, date
from services import UserService, IntentService, AppointmentService
from utils import get_content


class MasterMind(object):
    """ MasterMind class """    

    def __init__(self, user_service, text):
        """ Initializes a MasterMind instance """
        self._text = text
        self._user_service = user_service        
        self._lang = self._user_service.get_language()
        self._doc = nlp[self._lang](text.lower())       
        self._user_service.register_user_msg([self._text])  # Register user's message 
    
    @classmethod
    def from_telegram_msg(cls, tg_user, tg_text):
        """ Creates a MasterMind instance from a Telegram message's user and text """
        user_service = UserService.from_telegram_user(tg_user)
        return cls(user_service, tg_text)

    def get_response_for_telegram(self):
        """ Generates a response for the message with the Telegram format """
        responses = self._get_response()
        telegram_responses = list(map(lambda response: {
            'text': response,
            'parse_mode': 'HTML'
        }, responses))
        return telegram_responses
    
    def _get_response(self):
        """ Generates an adequate response """         
        try:
            if self._user_service.is_new_user:
                responses = [self._welcome_message()]
            else:
                responses = self._intent_driven_message()

        except Exception as e:
            app.logger.error(str(e))
            responses = [self._internal_error_message()]

        finally:            
            self._user_service.register_bot_msg(responses) # Register bot messages
            return responses

    def _welcome_message(self):
        """ Generates a welcome message in the corresponding language """
        return get_content(self._lang, ['welcome'])

    def _internal_error_message(self):
        """ Generates an internal error message in the corresponding language """
        return get_content(self._lang, ['internal_error'])

    def _intent_driven_message(self):
        """ Generates a intent-driven response for the message """
        responses = []
        errors = {}      
       
        # Set intent service 
        self._set_intent_service()
        intent_response = self._intent_service.get_response(self._doc)

        # Do action if there is one
        action = self._intent_service.get_action()
        if action: 
            intent_params = self._intent_service.get_params()
            errors = self._do_action(action, intent_params)

        if errors:
            responses.extend(list(map(lambda err: err, errors.values())))     
            self._intent_service.reset_params(**errors)
            self._invalidate_doc_entities()
            intent_response = self._intent_service.get_response(self._doc)

        # Save intent (if not completed)
        self._intent_service.save_intent()
        responses.append(intent_response)
        
        return responses
    
    def _set_intent_service(self):
        """ Identifies the intent of the message and creates an 
            IntentService """
        # Intent identification
        all_intents = self._doc.cats 
        
        # Check if there's an active intent
        active_intent = self._user_service.get_active_intent()  
        if active_intent:
            all_intents[active_intent.name] = 1 

        # Take intents priorities into account
        all_intents = dict(map(lambda kv: (kv[0], kv[1]*IntentService.priority(kv[0])), all_intents.items()))
        
        # Select the intent with the highest probability
        intent = max(all_intents, key=all_intents.get)            
        
        # Intent service creation 
        if active_intent and active_intent.name == intent:
            self._intent_service = IntentService.from_stored_intent(self._lang, active_intent)
        else:
            self._intent_service = IntentService.from_new_intent(self._lang, intent, self._user_service.user_id)

    def _invalidate_doc_entities(self):
        """ Invalidates the the doc """
        self._doc.ents = [] 

    def _do_action(self, name, params):
        """ Executes the corresponding action """
        errors = {}
        if name not in ACTIONS:
            raise AttributeError("Action '{}' is not a valid action".format(name))
        if name == 'deactivate_intent':
            errors = self._deactivate_intent(params)
        elif name == 'make_appointment':
            errors = self._make_appointment(params)

        return errors

    def _deactivate_intent(self, params):
        """ Deactivates the user's current intent"""
        errors = {}
        content = get_content(self._lang, ['deactivate_intent'])
        try:
            self._user_service.deactivate_intent()
        except Exception:
            errors['main'] = content['error'].format(**params)
        else:
            return errors

    def _make_appointment(self, params):
        """ Makes an appointment if the established time is valid """
        errors = {}
        content = get_content(self._lang, ['make_appointment'])
        t_date = parse(params['date'], languages=[self._lang]).date()
        t_time =  parse(params['time'], languages=[self._lang]).time()
        t_datetime = datetime.combine(t_date, t_time)
        av_slots = AppointmentService.get_available_slots(t_date.isoformat())        

        # Parameters validation 
        if t_date < date.today():
            errors['date'] = content['past_date'].format(**params)

        elif not AppointmentService.office_is_open_on_date(t_date.isoformat()):
            errors['date'] = content['office_close_date'].format(**params)

        elif not av_slots:
            errors['date'] = content['not_available_date'].format(**params)
              
        elif t_datetime < datetime.now():
            errors['time'] = content['past_datetime'].format(**params)

        elif not AppointmentService.office_is_open_on_datetime(
                                            t_datetime.isoformat()):
            errors['time'] = content['office_close_time'].format(**params)
        
        elif not AppointmentService.is_available(t_datetime.isoformat()):
            errors['time'] = content['not_available_time'].format(**params)           

        if not errors:
            closest_datetime = AppointmentService.closest_half(t_datetime.isoformat())
            t_time = datetime.fromisoformat(closest_datetime).time()
            try:
                self._user_service.make_appointment(t_date, t_time, params['topic'])
            except Exception as e:
                app.logger.error(str(e))
                errors['main'] = content['error'].format(**params)      

        return errors
