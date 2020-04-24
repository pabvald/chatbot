from app import db
from datetime import datetime


class User(db.Model):
    """ User model """
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    lang = db.Column(db.String(5), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship("Message", cascade="all, delete-orphan")
    intents = db.relationship("Intent", cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", cascade="all, delete-orphan")

    def __init__(self, first_name, lang, default_id=None):
        """ Initializes a User instance. An id can be optionally provided """
        self.first_name = first_name
        self.lang = lang
        if default_id:
            self.id = default_id        

    def __repr__(self):
        """Obtains a representation of the User model """
        return '<User {}>'.format(self.id)
    