from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from intents import validate_intents, train_intents
from entities import validate_entities, train_entities
from knowledge import validate_knowledge, train_knowledge

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def intents(option):
    """ Manages all the actions regarding the intents"""

    if option == 'validate':
        validate_intents()
    elif option == 'train':
        train_intents()
    else:
        print("'{}' is not a valid option for the 'intents' command".format(option))


@manager.command
def entities(option):
    """ Manages all the actions regarding the entities """
    if option == 'validate':
        validate_entities()
    elif option == 'train':
        train_entities()
    else:
        print("'{}' is not a valid option for the 'entities' command".format(option))


@manager.command
def knowledge(option):
    """ Manages all the actions regarding the knowledge base """
    if option == 'validate':
        validate_knowledge()
    elif option == 'train':
        train_knowledge()
    else:
        print("'{}' is not a valid option for the 'knowledge' command".format(option))


if __name__ == '__main__':
    manager.run()
