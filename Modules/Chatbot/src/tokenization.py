import re
def get_tokens(text):
    punct = {',','.','!',':','؟','?','/','\\','-','_','=','(',')','{','}','[',']','#','+','<','>','\'','\"'}
    dictionary = {'د':"دكتور"}#to be continued
    w = " "
    for char in text:
        if char not in punct:
            w += char
        else:
            w += " "
    words_after_split = w.split()
    for index , word in enumerate(words_after_split):
        if word in dictionary.keys():
            w = dictionary[word]
            words_after_split.remove(word)
            words_after_split.append(w)
    return words_after_split
            
    