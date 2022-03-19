import lexical_analysis


while True:
    text = "صحينى الساعة 10 الصبح بكرا"
    words = lexical_analysis.word_tokenization(text)
    ent_dict = lexical_analysis.NER(text)
    basic_words = lexical_analysis.stemming(words)
    print(text)
    print(words)
    print(ent_dict)
    print(basic_words)
    print("تم")
    break
    
    
    
    


