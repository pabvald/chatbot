from app import db


class Intent(db.Model):
    """ Intent model """
    
    __tablename__ = 'intents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parameters = db.relationship("Parameter", cascade="all, delete-orphan")

    def __init__(self, name, user_id):
        """ Initializes an Intent instance """
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        """ Obtains a representation of the Intent model """
        return '<Intent, {}, {}>'.format(self.id, self.name)

    @property
    def completed(self):
        """ Determines if an intent is completed """
        return all(list(map(lambda par: par.obtained, self.parameters)))

    @property 
    def stored(self):
        """ Determines if an intent has been stored """
        return self.id is not None

    @property
    def required_parameters(self):
        """ Returns a list of the required and yet not obtained parameters """
        return list(filter(lambda par: (not par.obtained) and par.required, self.parameters))

    @property 
    def obtained_parameters(self):
        """ Returns a list of the already obtained parameters """ 
        return list(filter(lambda par: par.obtained, self.parameters))