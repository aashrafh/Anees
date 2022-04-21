import tokenization
import preprocess
#import ner
import verb_extraction

text = input()
#Preprocessing
text = preprocess.pre_process(text)
print(text)
#Tokenization
tokens = tokenization.get_tokens(text)
print(tokens)
tokens = verb_extraction.extract_stem_verb(tokens)
print(tokens)
# NER
#ents = ner.get_ents(tokens)
#print(ents)
# GloVe ---> Task
# Task

    
    
    


