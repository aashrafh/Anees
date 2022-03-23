import re
def get_tokens(text):
    dictionary = {'د':"دكتور"}#to be continued
    words_after_split = text.split()
    for index , word in enumerate(words_after_split):
        if word in dictionary.keys():
            w = dictionary[word]
            words_after_split.remove(word)
            words_after_split.append(w)
    return words_after_split
            
    