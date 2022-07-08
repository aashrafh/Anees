def get_tokens(text,stopwords):
    dictionary = {'د':"دكتور"}#to be continued
    words_after_split = text.split()
    for index , word in enumerate(words_after_split):
        if word in dictionary.keys():
            w = dictionary[word]
            words_after_split[index] = w
    new_words = list()
    for word in words_after_split:
        if word not in stopwords:
            new_words.append(word)
    return new_words