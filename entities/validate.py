#!/usr/bin/env python
# coding: utf-8


from entities import CUSTOM_ENTITIES, PATH_SCHEMA, PATH_DEFINITIONS
from jsonschema import validate
from utils import read_json


def main():
    """Validates the entities JSON files """
    schema = read_json(PATH_SCHEMA)   
    for intent in CUSTOM_ENTITIES:
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
