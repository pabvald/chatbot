from app import db


class Parameter(db.Model):
    """ Parameter model """
    
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    entity = db.Column(db.String(100), nullable=False)
    required = db.Column(db.Boolean, nullable=False)
    value = db.Column(db.String(100), nullable=True)
    original = db.Column(db.String(100), nullable=True)    
    intent_id = db.Column(db.Integer, db.ForeignKey('intents.id'), nullable=False)

    def __init__(self, name, required, entity):
        """ Initializes an Intent instance """
        self.name = name
        self.required = required
        self.entity = entity
        self.value = None
        self.original = None 

    def __repr__(self):
        """ Obtains a representation of the Parameter model """
        return '<Parameter, {}, {}>'.format(self.id, self.name)

    @property
    def obtained(self):
        """ Determines if the parameter's value has been obtained """
        return self.value is not None
