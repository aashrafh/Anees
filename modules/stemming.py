noun_prefix = {'ال', 'ب', 'ك', 'بال', 'كال', 'لل', 'و'}
noun_suffix = {'كن', 'كما', 'كم', 'هم', 'هن', 'هما'}


def stem(tokens_verb_noun):
    tokens_stemmed = list()
    for token in tokens_verb_noun:
        if token[1] != 'n':
            tokens_stemmed.append(token)
            continue
        noun = token[0]
        noun_length = len(noun)
        done = 0
        for prefix in noun_prefix:
            if noun_length - len(prefix) > 2 and noun[:len(prefix)] == prefix:
                tokens_stemmed.append((noun[len(prefix):], 'n'))
                done = 1
                break
        if not done:
            for suffix in noun_suffix:
                if noun_length - len(suffix) > 2 and noun[noun_length - len(suffix):] == suffix:
                    tokens_stemmed.append(
                        (noun[0: noun_length - len(suffix)], 'n'))
                    done = 1
                    break
        if not done:
            tokens_stemmed.append(token)
    return tokens_stemmed
