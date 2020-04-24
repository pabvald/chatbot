#!/usr/bin/env python
# coding: utf-8

"""Train a convolutional neural network text classifier on the
IMDB dataset, using the TextCategorizer component. The dataset will be loaded
automatically via Thinc's built-in dataset loader. The model is added to
spacy.pipeline, and predictions are available via `doc.cats`. For more details,
see the documentation:
* Training: https://spacy.io/usage/training

Compatible with: spaCy v2.0.0+
"""

import operator
import random
import spacy

from brain import LANGUAGES, PATH_MODELS
from intents import INTENTS, PATH_DEFINITIONS
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from spacy.util import minibatch, compounding, decaying
from utils import read_json

TEST_TEXTS = {
    "en": [
        "Hello!",
        "Good bye, bot!",
        "Where can I get my UVA card ?",
        "Hey",
        "Bye, bot!",
        "can you help me ?",
        "I want to make an appointment",
        "cancel it"
    ],

    "es": [
        "Hola!",
        "Adiós, bot",
        "¿Dónde puedo conseguir mi tarjeta UVA?",
        "Buenas",
        "Necesito ayuda",
        "Quiero concertar una cita",
        "cancelalo"
    ] 
}  


def evaluate(tokenizer, textcat, texts, cats):
    """ Evaluates the text classifier over a set of examples and provides
        a text report showing the main classification metrics (precision, 
        recall, f1-score, support) """
    cats_pred = []
    docs = (tokenizer(text) for text in texts)
    y_true = list(map(lambda c: max(c.items(), key=operator.itemgetter(1))[0], cats))
    y_true = list(map(lambda t: INTENTS.index(t), y_true))
    
    for doc in textcat.pipe(docs):
        cats_pred.append(doc.cats)
        
    y_pred = list(map(lambda c: max(c.items(), key=operator.itemgetter(1))[0], cats_pred))
    y_pred = list(map(lambda t: INTENTS.index(t), y_pred))
    
    return classification_report(y_true, y_pred, target_names=INTENTS)


def load_data(lang, limit=0.0, split=0.85):
    """Loads the intents definitions """
    train_data = []
    
    for intent in INTENTS:
        file_path = '{}/{}.json'.format(PATH_DEFINITIONS, intent)
        data = read_json(file_path)
        train_data += list(map(lambda text: (text, intent), data['training_phrases'][lang]))
   
    texts, labels = zip(*train_data)
    cats = list(map(lambda y: dict(map(lambda intent: (intent, intent == y), INTENTS)), labels))
    
    if split < 1.0:
        texts_train, texts_dev, cats_train, cats_dev = train_test_split(texts, 
                                                                        cats, 
                                                                        train_size=split, 
                                                                        shuffle=True, 
                                                                        stratify=labels)
    else:
        texts_train = texts 
        cats_train = cats 
        texts_dev = []
        cats_dev = []
    return (texts_train, cats_train), (texts_dev, cats_dev)


def main(n_iter=20, init_tok2vec=None, split=1.0):
    """ Loads the model, trains the text classifier, saves the model and tests it """
    
    for lang in LANGUAGES:
        # Load model 
        print("Loading model '{}'...".format(lang))
        model_path = '{}/{}'.format(PATH_MODELS, lang)
        nlp = spacy.load(model_path)

        # Add a new text classifier to the pipeline.
        textcat = nlp.create_pipe(
                "textcat", config={"exclusive_classes": True, "architecture": "ensemble"}
            )
        if "textcat" not in nlp.pipe_names:
            print("Adding textcat pipe")        
            nlp.add_pipe(textcat, last=True)
        else:
            print("Replacing textcat pipe")
            nlp.replace_pipe("textcat", textcat)

        # Add labels to text classifier
        for intent in INTENTS:
            textcat.add_label(intent)

        # Load the intents definitios
        print("Loading data...")
        (train_texts, train_cats), (dev_texts, dev_cats) = load_data(lang, split=split)
        print("Intents: ", INTENTS)
        print(
            "Using {} examples ({} training, {} evaluation)".format(
                (len(train_texts) + len(dev_texts)), len(train_texts), len(dev_texts)
            )
        )
        train_data = list(zip(train_texts, [{"cats": cats} for cats in train_cats]))

        # Get names of other pipes to disable them during training
        pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

        with nlp.disable_pipes(*other_pipes):  # only train textcat
            if init_tok2vec is not None:
                with init_tok2vec.open("rb") as file_:
                    textcat.model.tok2vec.from_bytes(file_.read())
           
            optimizer = nlp.begin_training()
            dropout = decaying(0.6, 0.2, 0.02)
            batch_sizes = compounding(1.0, 3.0, 1.001)

            print("Training the model...")
            for i in range(n_iter):
                losses = {}
                # batch up the examples using spaCy's minibatch
                random.shuffle(train_data)
                drop = next(dropout)
                batches = minibatch(train_data, size=batch_sizes)
                for batch in batches:
                    texts, annotations = zip(*batch)                    
                    nlp.update(texts, annotations, sgd=optimizer, losses=losses, drop=drop)
                print("ITERATION ", i)
                print(">>LOSS:", losses["textcat"])
                if dev_texts:
                    with textcat.model.use_params(optimizer.averages):
                        # Evaluate on the dev data split off in load_data()
                        classification_report = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
                    print(">>Classfication report")
                    print(classification_report)
                print("\n")

        # Test the trained model    
        for doc in nlp.pipe(TEST_TEXTS[lang]):
            print(doc.doc, doc.cats)

        # Save model to disk
        print("Saving model to disk ...")
        nlp.to_disk(model_path)
        print("")


if __name__ == "__main__":
    main()