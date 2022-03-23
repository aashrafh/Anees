#import lexical_analysis
import tokenization
import preprocess

# while True:
#     text = input()
#     words = lexical_analysis.word_tokenization(text)
#     ent_dict = lexical_analysis.NER(text)
#     basic_words = lexical_analysis.stemming(words)
#     task = lexical_analysis.similar.sim(text)
#     # print(text)
#     # print(words)
#     # print(ent_dict)
#     # print(basic_words)
#     print(task)
#     print("تم")
#     break


text = " . أحمد  دفعت 10 جنية فى مصر ؟ د.هحمد الساعة 10"
text = preprocess.remove_punctuations(text)
text = preprocess.remove_diacritics(text)
text = preprocess.normalize_arabic(text)
tokens = tokenization.get_tokens(text)
print(tokens)
    
    
    


