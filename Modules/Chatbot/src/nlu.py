import lexical_analysis

def understanding(text):
    words = lexical_analysis.word_tokenization(text)[0:5]
    print(words)
    words = lexical_analysis.stemming(words)
    print(words)