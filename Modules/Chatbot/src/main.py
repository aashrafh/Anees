import lexical_analysis


while True:
    text = input()
    words = lexical_analysis.word_tokenization(text)
    ent_dict = lexical_analysis.NER(text)
    basic_words = lexical_analysis.stemming(words)
    task = lexical_analysis.similar.sim(text)
    # print(text)
    # print(words)
    # print(ent_dict)
    # print(basic_words)
    print(task)
    print("تم")
    break
    
    
    
    


