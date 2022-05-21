from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

labels = ['sports','schedule','general','weather','recommendation','greeting','thank']

max_length = 200
training_portion = 0.8
def intent(text):
    m = keras.models.load_model("Intent_Classification/models")
    filename = f'../utils/tokenizer.sav'
    tokenizer = pickle.load(open(filename, 'rb'))
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_length)
    pred = m.predict(padded)
    try:
        label = labels[np.argmax(pred)-1] 
    except:
        label = 'general'
    print(label)