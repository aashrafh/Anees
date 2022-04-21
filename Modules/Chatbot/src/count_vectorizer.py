import numpy as np
from tokenization import get_tokens

class CountVectorizer:
    def __init__(self) -> None:
        self.__vocabulary = {}
        self.__vocab_count = 0
        pass

    def fit(self, docs : list) -> None:
        for doc_i in range(len(docs)):
            tokens = get_tokens(docs[doc_i])
            for token in tokens:
                if self.__vocabulary.get(token) == None:
                    self.__vocabulary[token] = self.__vocab_count
                    self.__vocab_count += 1

    def transform(self, docs : list) -> list:
        freq = np.zeros((len(docs), self.__vocab_count), dtype="int")
        for doc_i in range(len(docs)):
            tokens = get_tokens(docs[doc_i])
            for token in tokens:
                freq[doc_i , self.__vocabulary[token]] += 1
        return freq.tolist()

    def get_vocab_count(self) -> int:
        return self.__vocab_count
    
    def get_vocab(self) -> list:
        return self.__vocabulary
        