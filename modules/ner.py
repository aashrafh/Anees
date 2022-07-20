import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
import pandas as pd
# from count_vectorizer import CountVectorizer
from config import *


class NER:
    def __init__(self):
        self.train_dataframe = NER.textfile_to_dataframe(
            file=open(ANER_PATH, encoding='utf-8'))
        self.train()

    def train(self):
        words = self.train_dataframe['text'].astype(str)
        labels = self.train_dataframe['label'].astype(str)

        vectorizer = CountVectorizer()
        linear_svc_model = LinearSVC()

        vectorizer.fit(words)
        vectorizer_matrix = vectorizer.transform(words)

        linear_svc_model.fit(vectorizer_matrix, labels)

        self.vectorizer = vectorizer
        self.predictor = linear_svc_model

    def predict(self, word):
        test_str = self.vectorizer.transform([word])
        return self.predictor.predict(test_str.toarray())[0]

    def textfile_to_dataframe(file, col1="text", col2="label"):
        texts = []
        labels = []

        lines = file.readlines()
        lines = [line.replace('\n', '').split(" ") for line in lines]
        tmp = []
        for l in lines:
            if len(l) == 2:
                tmp.append(l)
        lines = np.array(tmp)

        texts = lines[:, 0]
        labels = lines[:, 1]

        csv_file = pd.DataFrame({col1: texts, col2: labels})
        return csv_file


def get_ents(tokens, ner_instance):
    ents = dict()
    for token in tokens:
        ent_type = ner_instance.predict(token)
        if ent_type != 'O':
            ents[token] = ent_type
    return ents
