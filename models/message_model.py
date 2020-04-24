import enum
from app import db
from datetime import datetime


class MessageType(enum.Enum):
    """ MessageType class """
    
    USER = 'user'
    BOT = 'bot'


class Message(db.Model):
    """ Message model class """

    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    msg_type = db.Column(db.Enum(MessageType), nullable=False)
    text = db.Column(db.Text, nullable=False)
    d_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, msg_type, user_id):
        """ Initializes a Message instance"""
        self.text = text
        self.d_time = datetime.utcnow()
        self.msg_type = msg_type
        self.user_id = user_id

    def __repr__(self):
        """ Obtains a string representation of the instance """
        return '<Message {}>'.format(self.id)