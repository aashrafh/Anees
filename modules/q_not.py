def get_q_not(text, model, tf_idf):
    text0 = tf_idf.transform([text])
    q_not = model.predict(text0)[0]
    return q_not
