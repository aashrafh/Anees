import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

labels = ['movies','locations']

max_length = 200
training_portion = 0.8
def intent(text):
    m = keras.models.load_model("Recommendation_intent/intent/movie_location_model")
    filename = f'../utils/recomm_tokenizer.sav'
    tokenizer = pickle.load(open(filename, 'rb'))
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_length)
    pred = m.predict(padded)
    try:
        label = labels[np.argmax(pred)-1] 
    except:
        label = 'general'
    return label