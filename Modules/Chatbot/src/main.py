import lexical_analysis
import tokenization

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


text = " .   دفعت 10 جنية في مصر ؟ د.هحمد الساعة 10"
#preprocessing kol el 7roof ely shbah b3d n5lehom 7aga w7da
words = tokenization.get_tokens(text)
#stopwords n5tar ely m7tageno
print(lexical_analysis.remove_stopwards(words))  
print(lexical_analysis.stemming(words))  
#similarity show what task it is 
#task
    
    
    


