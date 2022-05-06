import tokenization
import preprocess
import ner
import verb_extraction
import stemming
import sentimental_analysis


text = input()
#Preprocessing
text = preprocess.pre_process(text)
print(text)
emotion = sentimental_analysis.get_emotion(text)
print(emotion)
#Tokenization
tokens = tokenization.get_tokens(text)
print(tokens)
# NER
ents = ner.get_ents(tokens)
print(ents)
#Part of Speech and Stemming
tokens_verb_noun = verb_extraction.extract_stem_verb(tokens,ents)
print(tokens_verb_noun)
tokens_verb_noun = stemming.stem(tokens_verb_noun)
print(tokens_verb_noun)
# GloVe ---> Task
# Task

    
    
    


