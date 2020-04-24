#!/usr/bin/env python
# coding: utf-8

import spacy
from brain import LANGUAGES, PATH_MODELS
from entities import PATH_DEFINITIONS, CUSTOM_ENTITIES
from spacy.pipeline import EntityRuler
from utils import read_json


def load_data(lang):
    """ Loads the entities definitions stored in the JSON files """
    definitions = {}
    for entity in CUSTOM_ENTITIES:
        file_path = './{}/{}.json'.format(PATH_DEFINITIONS, entity)
        data = read_json(file_path)
        definitions[data['label']] = data['entries']
    return definitions 


def main():
    """ Adds an EntityRuler to the spacy models to recognize the custom 
        entities """
    for lang in LANGUAGES:
        patterns = []

        # Load entities' definitions
        print("Custom entities: ", CUSTOM_ENTITIES)
        entities = load_data(lang)

        # Load model 
        print("Loading model '{}'...".format(lang))
        model_path = '{}/{}'.format(PATH_MODELS, lang)
        nlp = spacy.load(model_path)

        # Create patterns 
        print("Generating patterns...")
        for (label, entries) in entities.items():
            for entry in entries:
                for patt in entry['patterns'][lang]:
                    patterns.append({"label": label, "pattern": patt, "id": entry['id']})         

        # Create EntityRuler with patterns 
        print("Creating EntityRuler...")
        entity_ruler = EntityRuler(nlp, overwrite_ents=True, validate=True)
        entity_ruler.add_patterns(patterns)

        # Add EntityRuler to pipeline
        if "entity_ruler" not in nlp.pipe_names:
            nlp.add_pipe(entity_ruler)
        else:
            nlp.replace_pipe("entity_ruler", entity_ruler)
        print("EntityRuler added to /{}'s pipeline".format(lang))

        # Save model to disk
        print("Saving model to disk ...")
        nlp.to_disk(model_path)
        print("")


if __name__ == '__main__':
    main()
