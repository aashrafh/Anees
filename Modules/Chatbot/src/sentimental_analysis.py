from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def get_emotion(text):
    filename = f'../utils/sentmental_model.sav'
    model = pickle.load(open(filename, 'rb'))
    filename = f'../utils/tfidf_model.sav'
    tf_idf = pickle.load(open(filename, 'rb'))
    text = tf_idf.transform([text]).toarray()
    emotion = model.predict(text)
    return emotion[0]
    