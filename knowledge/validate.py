#!/usr/bin/env python
# coding: utf-8


from brain import LANGUAGES
from jsonschema import validate
from knowledge import PATH_SCHEMA, PATH_KNOWLEDGE_BASE
from utils import read_json


def main():
    """Validates the knowledge JSON files """
    schema = read_json(PATH_SCHEMA)   
    for lang in LANGUAGES:
        data_path = '{}/{}.json'.format(PATH_KNOWLEDGE_BASE, lang)        
        data = read_json(data_path)
        try:
            validate(instance=data, schema=schema)
            print("'{}.json' is valid".format(lang))
        except Exception as err:
            print("'{}.json' is NOT valid".format(lang))
            print(err)


if __name__ == '__main__':
    main()
