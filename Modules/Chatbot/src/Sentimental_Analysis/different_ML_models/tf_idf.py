import pandas as pd
import numpy as np
import tokenization

class  TF_IDF:
    def __init__(self,ngram,max_df,min_df):
        self.ngram = ngram
        self.max_df = max_df
        self.min_df = min_df
        
    def tf(self,word,text_index):
        tokens = self.tokens_list[text_index]
        tf = 0
        for token in tokens:
            if token == word:
                tf += 1
        return tf/(len(tokens)+1)
    
    def df(self,word):
        df = 0
        for i in range(len(self.text_list)):
            tokens = self.tokens_list[i]
            if word in tokens:
                df += 1
        return df
    
    def idf(self,word):
        N = len(self.text_list)
        df_value = self.df(word)
        idf = np.log(N/(df_value+1))
        return idf
    
    def fit_transform(self,text_list):
        words = set()
        tokens_list = list()
        for i in range(len(text_list)):
            tokens = tokenization.get_tokens(text_list[i])
            words.update(set(tokens))
            tokens_list.append(tokens)
        self.words = list(words)
        self.text_list = text_list
        self.tokens_list = tokens_list
        return self.transform(text_list, True)
        
    def transform(self,text_list,train = False):
        self.text_list = text_list
        if not train: 
            tokens_list = list()
            for i in range(len(text_list)):
                tokens = tokenization.get_tokens(text_list[i])
                tokens_list.append(tokens)
            self.tokens_list = tokens_list
        tf_idf_list = list()
        idf_list = [self.idf(word) for word in self.words]
        for i in range(len(self.text_list)):
            tf_idf = list()
            for index , word in enumerate(self.words):
                tf_idf.append(self.tf(word,i)*idf_list[index])
            tf_idf_list.append(tf_idf)
        tf_idf_list = np.array(tf_idf_list)
        data_dict = dict()
        for i in range(len(self.words)):
            data_dict[self.words[i]] = tf_idf_list[:,i]
        data = pd.DataFrame(data_dict)
        return data
    
    
    
