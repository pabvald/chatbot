from utils import read_json
from jsonschema import validate
from intents import INTENTS, PATH_SCHEMA, PATH_DEFINITIONS

def main():
    """Validates the intents JSON files """
    schema = read_json(PATH_SCHEMA)
    for intent in INTENTS:
        data_path = '{}/{}.json'.format(PATH_DEFINITIONS, intent)
        data = read_json(data_path)
        try:
            validate(instance=data, schema=schema)
            print("'{}.json' is valid".format(intent))
        except Exception as err:
            print("'{}.json' is NOT valid".format(intent))
            print(err)

if __name__ == '__main__':
    main()
