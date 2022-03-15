import lexical_analysis

def understanding(text):
    word = lexical_analysis.word_tokenization(text)[0]
    print(word)