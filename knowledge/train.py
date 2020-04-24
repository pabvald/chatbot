#!/usr/bin/env python
# coding: utf-8

import spacy
import numpy as np 
from brain import LANGUAGES, PATH_MODELS
from utils import save_as_json, read_json
from knowledge import PATH_KNOWLEDGE_BASE


def sentence_embedding(nlp, sentences, punctuation=False, stop_words=False):
    """ Computes the embeddings of a list of sentences, omitting 
        stop words and punctuation symbols """
    sentence_embeddings = [] 
    
    for doc in nlp.pipe(sentences):    
        tokens = list(filter(lambda t: t.has_vector and (not t.is_punct) and (not t.is_stop), doc.doc)) 
        vectors = list(map(lambda t: t.vector, tokens))
        embedding = np.average(vectors, axis=0)
        sentence_embeddings.append(embedding)        
    
    return np.array(sentence_embeddings)


def main():
    """ Computes the embeddings of the stored Questions """
    for lang in LANGUAGES:
        # Load model
        print("Loading '{}' model... ".format(lang))
        model_path = '{}/{}'.format(PATH_MODELS, lang)
        nlp = spacy.load(model_path, disable=["parser", "ner", "textcat"])

        # Read QA pairs
        print("Reading '{}' knowledge base...".format(lang))
        data_path = '{}/{}.json'.format(PATH_KNOWLEDGE_BASE, lang)
        qa_pairs = read_json(data_path)

        # Generate the embeddings of the Questions
        print("Generating sentence embeddings...")
        questions = list(map(lambda pair: pair['question'].lower(), qa_pairs))
        q_embeddings = sentence_embedding(nlp, questions)
        for i in range(len(qa_pairs)):
            pair = qa_pairs[i]
            pair['embedding'] = q_embeddings[i].tolist()

        # Save the model
        print("Saving '{}' knowledge base....".format(lang))
        save_as_json(data_path, qa_pairs)
        print("")


if __name__ == '__main__':
    main()