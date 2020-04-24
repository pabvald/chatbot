from app import db
from datetime import datetime


class Appointment(db.Model):
    """ Appointment model """
    
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    d_time = db.Column(db.DateTime, nullable=False)
    topic = db.Column(db.String(60), nullable=False)    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, date, time, topic, user_id):
        """ Initializes an Appointment instance """
        self.d_time = datetime.combine(date, time)
        self.topic = topic
        self.user_id = user_id

    def __repr__(self):
        """ Obtains a representation of the Appointment model """
        return '<Appointment, {}, {}, {}, {}>'.format(self.id, self.date, self.time, self.affair)

    @property 
    def date(self):
        """ Obtains the date of the appointment """
        return self.d_time.date()

    @property
    def time(self):
        """ Obtains the time (hour, minute, second) of the 
            appointment """ 
        return self.d_time.time()  

    @property
    def passed(self):
        """ Determines if an appointment has passed """
        return  self.d_time < datetime.utcnow() 

    @property
    def pending(self):
        """ Determines if an appointment is pending """
        return  self.d_time > datetime.utcnow() 

    @property
    def weekday(self):
        """ Obtains the weekday as an integer in the range [0,6] """
        return self.d_time.weekday()
