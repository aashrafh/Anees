import tokenization
import preprocess
#import ner
import verb_extraction
import stemming

text = input()
#Preprocessing
text = preprocess.pre_process(text)
print(text)
#Tokenization
tokens = tokenization.get_tokens(text)
print(tokens)
tokens_verb_noun = verb_extraction.extract_stem_verb(tokens)
print(tokens_verb_noun)
tokens_verb_noun = stemming.stem(tokens_verb_noun)
print(tokens_verb_noun)
# NER
#ents = ner.get_ents(tokens)
#print(ents)
# GloVe ---> Task
# Task

    
    
    


