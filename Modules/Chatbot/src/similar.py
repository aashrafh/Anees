import spacy
from nltk.corpus import stopwords
nlp = spacy.load('en_core_web_lg')

def sim(text):
    text_train = 'weather schedule'
    doc = nlp(text)
    tokens1 = list()
    stop_words = set(stopwords.words('english'))
    for t in doc:
        if str(t) not in stop_words and str(t).isalpha():
            tokens1.append(t)
    tokens2 = nlp(text_train)
    task = [0,0]
    for t1 in tokens1:
        print(str(t1))
        for index , t2 in enumerate(tokens2):
            print(t2.similarity(t1))
            task[index] += t2.similarity(t1)
    wanted_task = tokens2[task.index(max(task))]
    return wanted_task