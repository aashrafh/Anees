from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def get_emotion(text):
    filename = f'../utils/sentmental_+-_model.sav'
    model = pickle.load(open(filename, 'rb'))
    filename = f'../utils/tfidf_+-_model.sav'
    tf_idf = pickle.load(open(filename, 'rb'))
    text0 = tf_idf.transform([text])
    pos_neg = model.predict(text0)[0]
    filename = f'../utils/sentmental_pos_model.sav'
    model_pos = pickle.load(open(filename, 'rb'))
    filename = f'../utils/tfidf_pos_model.sav'
    tf_idf_pos = pickle.load(open(filename, 'rb'))
    filename = f'../utils/sentmental_neg_model.sav'
    model_neg = pickle.load(open(filename, 'rb'))
    filename = f'../utils/tfidf_neg_model.sav'
    tf_idf_neg = pickle.load(open(filename, 'rb'))
    if pos_neg == 'pos':
        tweet = tf_idf_pos.transform([text])
        return model_pos.predict(tweet)[0]
    else:
        tweet = tf_idf_neg.transform([text])
        return model_neg.predict(tweet)[0]
    