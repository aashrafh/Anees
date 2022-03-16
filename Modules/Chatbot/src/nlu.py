import lexical_analysis

def understanding(text):
    words = lexical_analysis.word_tokenization(text)[0:14]
    print(words)
    words = lexical_analysis.remove_stopwards(words)
    print(words)
    words = lexical_analysis.stemming(words)
    print(words)