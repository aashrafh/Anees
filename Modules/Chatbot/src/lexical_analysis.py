import nltk
import spacy
import arabicstopwords.arabicstopwords as stp
nlp = spacy.load('en_core_web_sm')

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
def NER (text):
    doc = nlp(text)
    ner_dict = dict()
    for ent in doc.ents:
        ner_dict[ent.text] = ent.label_
    return ner_dict
def remove_stopwards(words):
    new_words = list()
    for word in words:
        if word not in stp.stopwords_list():
            new_words.append(word)
    return new_words