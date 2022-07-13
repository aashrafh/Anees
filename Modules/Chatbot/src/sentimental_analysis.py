def get_emotion(text,model,tf_idf):
    text0 = tf_idf.transform([text])
    emotion = model.predict(text0)[0]
    return emotion
    