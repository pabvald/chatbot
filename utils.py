""" 
    Common utilities.
"""
import json
import yaml
from app import app


PATH_CONTENT = 'content'


def save_as_json(file_name, data):
    """ Saves the provided data as a JSON file """
    try:
        with open(file_name, 'w', encoding='utf8') as fout:
            json.dump(data , fout, indent=4, sort_keys=True, ensure_ascii=False)
    except Exception as e:
        app.logger.error("saving file '{}' - {}".format(file_name, str(e)))
        raise


def save_as_jsonl(file_name, dicts):
    """ Saves a list of dictionaries as JSONL file """
    try:
        with open(file_name, 'w') as fout:
            for d in dicts:
                json.dump(d, fout)
                fout.write('\n')
    except Exception as e:
        app.logger.error("saving file '{}' - {}".format(file_name, str(e)))
        raise


def read_json(file_name):
    """ Reads a JSON file and returns its content """
    try:
        with open(file_name, 'r', encoding='utf8') as fin:
            data = json.load(fin)
    except Exception as e:
        app.logger.error("reading file '{}' - {}".format(file_name, str(e)))
        raise
    else:
        return data


def read_yaml(file_name):
    """ Reads a YAML file and returns its content """
    try:
        with open(file_name, 'r') as fin:
            data = yaml.safe_load(fin)
    except Exception as e:
        app.logger.error("reading file '{}' - {}".format(file_name, str(e)))
        raise
    else:
        return data


def get_content(lang, keys):
    """ Gets a content in the corresponding language """ 
    file_name = '{}/{}.yaml'.format(PATH_CONTENT, lang)
    data = read_yaml(file_name)    
    try:
        for k in keys:
            data = data[k]
    except Exception as e:
        app.logger.error("in '{}' content - {}".format(lang, str(e)))
        raise
    else:
        return data
