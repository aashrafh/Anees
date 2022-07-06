from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def get_emotion(text):
    filename = f'Sentimental_Analysis/models/sentmental_all_model.sav'
    model = pickle.load(open(filename, 'rb'))
    filename = f'Sentimental_Analysis/models/tfidf_all_model.sav'
    tf_idf = pickle.load(open(filename, 'rb'))
    text0 = tf_idf.transform([text])
    emotion = model.predict(text0)[0]
    print(emotion)
    return emotion
    