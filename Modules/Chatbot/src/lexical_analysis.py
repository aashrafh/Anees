import nltk

def word_tokenization(data):
    words = nltk.tokenize.word_tokenize(data)
    return words
def sentence_tokenization(data):
    sents = nltk.tokenize.sent_tokenize(data)
    return sents
def part_of_speech(text):
    word_type = dict()
    for  w , t in nltk.pos_tag(word_tokenization(text)):
        word_type[w] = t
    return word_type
def stemming(words):
    stem = list()
    s_stemmer = nltk.stem.ISRIStemmer()
    for word in words:
        stem.append(s_stemmer.stem(word))
    return stem