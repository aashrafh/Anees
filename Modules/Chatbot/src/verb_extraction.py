verb_prefix = {'فسن','فست','فسي','فا','سي','ست','سن','سا','فن','فت','في','فس','س','ف','ن','ت','ي','ا',''}
verb_suffix = {'ى','تما','ا','ت','ين','ان','و','وا','تن','تم','تا','نا','ون','ن',''}
def verb_dictionary():
    file = open("../Data/verb_dictionary.txt","r",encoding="utf-8")
    verbs = file.read().split()
    file.close()
    return verbs
def extract_stem_verb(tokens):
    verbs = verb_dictionary()
    tokens_stemmed = list()
    for token in tokens:
        len_token = len(token)
        if len_token < 4:
            if token in verbs:
                tokens_stemmed.append((token,"v"))
            else:
                tokens_stemmed.append((token,"nv"))
            continue
        token_stemmed = token
        is_verb = "nv"
        print(token)
        for prefix in verb_prefix:
            for suffix in verb_suffix:
                if len(token) - len(prefix) - len(suffix) > 0 and token[: len(prefix)] == prefix and token[len(token) - len(suffix) : ] == suffix:
                    token_possible_stem = token[len(prefix) : len(token) - len(suffix) ]
                    print (token_possible_stem)
                    if token_possible_stem in verbs and len(token_possible_stem) < len(token_stemmed):
                        print(token_possible_stem)
                        token_stemmed = token_possible_stem
                        is_verb = "v"
        tokens_stemmed.append((token_stemmed,is_verb))
                        
    return tokens_stemmed