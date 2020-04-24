from app import app, db
from brain import LANGUAGES 
from datetime import datetime
from models import User, Appointment, Message, MessageType


class UserService(object):
    """ UserService class. """

    def __init__(self, user_id, new_user):
        """ Initializes an UserService instance """
        self.user_id = user_id 
        self.is_new_user = new_user

    @classmethod
    def from_telegram_user(cls, tg_user):
        """ Obtains the corresponding system User or creates a new one if it doesn't exist """
        try:
            new_user = False
            user = db.session.query(User).get(tg_user.id) 
                       
            if not user:
                new_user = True
                tg_lang_code = tg_user.language_code[0:2]
                if tg_lang_code in LANGUAGES:
                    user_lang = tg_lang_code 
                else:
                    user_lang = LANGUAGES[0]

                user = User(tg_user.first_name, user_lang, default_id=tg_user.id)
                db.session.add(user) 
                db.session.commit()

        except Exception as e:
            app.logger.error(str(e))
            raise
        else:
            return cls(user.id, new_user)

    def register_bot_msg(self, texts):
        """ Registers a Bot message """ 
        try:
            for text in texts:
                msg = Message(text, MessageType.BOT, self.user_id)
                db.session.add(msg)
            db.session.commit()
        except Exception as e:
            app.logger.error(str(e))
            raise

    def register_user_msg(self, texts):
        """ Registers a User message """
        try:
            for text in texts:
                msg = Message(text, MessageType.USER, self.user_id)
                db.session.add(msg)
            db.session.commit()
        except Exception as e:
            app.logger.error(str(e))
            raise

    def has_active_intent(self):
        """ Determines if the corresponding user has any active intent """
        try:
            user = db.session.query(User).get(self.user_id)
            active_intents = list(filter(lambda intent: not intent.completed, user.intents))
        except Exception as e:
            app.logger.error(str(e))
            raise
        else:
            return active_intents != []

    def get_language(self):
        """ Gets the language of he user """
        try:
            user = db.session.query(User).get(self.user_id)
        except Exception as e:
            app.logger.error(str(e))
            raise
        else:
            return user.lang

    def get_active_intent(self):
        """ Obtains the last stored intent of the corresponding user.
            Returns None if the corresponding user doesn't have any 
            active intent """
        try:
            user = db.session.query(User).get(self.user_id)
            user_intents = user.intents
        except Exception as e:
            app.logger.error(str(e))
            raise
        else:
            intent = None
            active_intents = list(filter(lambda i: not i.completed, user_intents))
            if active_intents:
                intent = active_intents[-1]
            return intent

    def deactivate_intent(self):
        """ Removes a user's active intents""" 
        try:
            active_intent = self.get_active_intent() 
            if active_intent:
                db.session.delete(active_intent)
                db.session.commit()
        except Exception as e:
            app.logger.error(str(e))
            raise

    def make_appointment(self, t_date, t_time, topic):
        """ Makes an appointment for the user. """
        try:
            appointment = Appointment(t_date, t_time, topic, self.user_id)
            db.session.add(appointment)
            db.session.commit()
        except Exception as e:
            app.logger.error(str(e))
            raise

    def get_appointments(self):
        """ Returns all user's appointments """
        try:
            user = db.session.query(User).get(self.user_id)
            appointemnts = user.appointments
        except Exception as e:
            app.logger.error(str(e))
            raise
        else:
            return appointemnts
