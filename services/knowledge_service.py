import numpy as np
from knowledge import PATH_KNOWLEDGE_BASE
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
from utils import read_json

class KnowledgeService(object):
    """ KnowledgeService class """

    def __init__(self, lang, threshold=0.7):
        """ Initializes an KnowledgeService instance """
        self.lang = lang
        self.knowledge = KnowledgeService._load_knowledge(lang)
        self.threshold = threshold

    @staticmethod
    def _sentence_embedding(question):
        """ Computes the embedding of a question, removing the punctuation 
            symbols and stop words """
        tokens = list(filter(lambda t: t.has_vector and (not t.is_punct) and (not t.is_stop), question.doc))
        vectors = list(map(lambda t: t.vector, tokens))
        embedding = np.average(vectors, axis=0)

        return embedding

    @staticmethod
    def _load_knowledge(lang):
        """ Reads a knowledge JSON file and returns its content """
        fpath = '{}/{}.json'.format(PATH_KNOWLEDGE_BASE, lang)
        data = read_json(fpath)
        return data

    def _most_similar_questions(self, request_question, n=1):
        """ Obtains the n most similar questions and its similarity to a given
            question """
        request_embedding = KnowledgeService._sentence_embedding(request_question)
        for pair in self.knowledge:
            pair['sim'] = cos_sim(np.array(pair['embedding']).reshape(1, -1), request_embedding.reshape(1, -1))
        sorted_qa_pairs = sorted(self.knowledge, key=lambda p: p['sim'], reverse=True)

        return sorted_qa_pairs[0:n]

    def get_response(self, msg):
        """ Determines the most similar question and provides its answer """
        response = None
        ms = self._most_similar_questions(msg)[0]
        if ms['sim'] >= self.threshold:
            response = ms['answer']
        return response
