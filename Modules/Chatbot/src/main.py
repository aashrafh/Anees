import tokenization
import preprocess

text = " . أحمد  دفعت 10 جنية فى مصر ؟ د.هحمد الساعة 10"
text = preprocess.pre_process(text)
tokens = tokenization.get_tokens(text)
# NER
# GloVe ---> Task
# Task
print(tokens)
    
    
    


