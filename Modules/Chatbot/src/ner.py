import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.svm import LinearSVC
# from count_vectorizer import CountVectorizer

class NER:
    def __init__(self):
        path = "../Data/ANERCorp_CamelLab_train.txt"
        self.train_dataframe = NER.textfile_to_dataframe(file=open(path, encoding='utf-8'))
        print(1)
        self.train()

    def train(self):
        df = self.train_dataframe

        train = df
        
        train_arr = []
        train_lbl = []
        print(2)
        train_arr=train['text'].astype(str)
        train_lbl=train['label'].astype(str)

        vectorizer = CountVectorizer()
        print(3)
        vectorizer.fit(train_arr)
        print(4)
        train_mat = vectorizer.transform(train_arr)
        print(5)

        tfidf = TfidfTransformer()
        tfidf.fit(train_mat)
        train_tfmat = tfidf.transform(train_mat)

        print(6)

        lsvm=LinearSVC()
        lsvm.fit(train_tfmat,train_lbl)

        print(7)

        self.vectorizer = vectorizer
        self.predictor = lsvm
        self.tfidf = tfidf
        
    def predict(self, word):
        test_str = self.vectorizer.transform([word])
        test_tfstr = self.tfidf.transform(test_str)
        return self.predictor.predict(test_tfstr.toarray())[0]

    def textfile_to_dataframe(file, col1="text", col2="label"):
        texts = []
        labels = []

        lines = file.readlines()
        lines =  [line.replace('\n', '').split(" ") for line in lines]
        tmp = []
        for l in lines:
            if len(l) == 2:
                tmp.append(l)
        lines = np.array(tmp)

        texts = lines[:,0]
        labels = lines[:,1]

        csv_file = pd.DataFrame({col1:texts, col2:labels})   
        return  csv_file

def get_ents(tokens,ner_instance):
    # new_ner = NER()
    # ents = dict()
    # for token in tokens:
    #     ent_type = new_ner.predict(token)
    #     if ent_type != 'O':
    #         ents[token] = ent_type
    # return ents
    ents = dict()
    for token in tokens:
        ent_type = ner_instance.predict(token)
        if ent_type != 'O':
            ents[token] = ent_type
    return ents