from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

labels = ['schedule','general','weather','recommendation','greeting','thank']
max_length = 200

def intent(text,m,tokenizer):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_length)
    pred = m.predict(padded)
    try:
        label = labels[np.argmax(pred)-1] 
    except:
        label = 'general'
    if label in ['thank' , 'greeting']:
        label = 'general'
    return label