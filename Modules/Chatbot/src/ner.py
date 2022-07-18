import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.svm import LinearSVC
import pandas as pd
# from count_vectorizer import CountVectorizer

class NER:
    def __init__(self):
        path = "../Data/ANERCorp_CamelLab_train.txt"
        self.train_dataframe = NER.textfile_to_dataframe(file=open(path, encoding='utf-8'))
        self.train()

    def train(self):
        words = self.train_dataframe['text'].astype(str)
        labels = self.train_dataframe['label'].astype(str)

        vectorizer = CountVectorizer()
        tf_idf = TfidfTransformer()
        linear_svc_model = LinearSVC()
        
        vectorizer.fit(words)
        vectorizer_matrix = vectorizer.transform(words)

        tf_idf.fit(vectorizer_matrix)
        tf_idf_matrix = tf_idf.transform(vectorizer_matrix)

        linear_svc_model.fit(tf_idf_matrix, labels)

        self.vectorizer = vectorizer
        self.predictor = linear_svc_model
        self.tf_idf = tf_idf
        
    def predict(self, word):
        test_str = self.vectorizer.transform([word])
        test_tfstr = self.tf_idf.transform(test_str)
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
    ents = dict()
    for token in tokens:
        ent_type = ner_instance.predict(token)
        if ent_type != 'O':
            ents[token] = ent_type
    return ents