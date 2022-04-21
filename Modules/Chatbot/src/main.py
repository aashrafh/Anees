import tokenization
import preprocess
import ner

text = " . أحمد  دفعت 10 جنية فى مصر ؟ د.هحمد الساعة 10"
#Preprocessing
text = preprocess.pre_process(text)
print(text)
#Tokenization
tokens = tokenization.get_tokens(text)
print(tokens)
# NER
# ents = ner.get_ents(tokens)
# print(ents)
# GloVe ---> Task
# Task

    
    
    


