import pos
verb_prefix = {'فسن','فست','فسي','فا','سي','ست','سن','سا','فن','فت','في','فس','س','ف','ن','ت','ي','ا',''}
verb_suffix = {'لي','ي','تما','ا','ت','ين','ان','و','وا','تن','تم','تا','نا','ون','ن',''}
def verb_dictionary():
    file = open("../Data/verb_dictionary.txt","r",encoding="utf-8")
    verbs = file.read().split()
    file.close()
    return verbs
def extract_stem_verb(tokens,ents):
    #no 2 verbs can appear after each other
    part_of_speech = pos.part_of_speech(tokens,ents)
    verbs = verb_dictionary()
    tokens_stemmed = list()
    for index , token in enumerate(tokens):
        if part_of_speech[index][1] != 'v':
            tokens_stemmed.append(part_of_speech[index])
            continue
        len_token = len(token)
        if len_token < 4:
            if token in verbs:
                tokens_stemmed.append((token,"v"))
            else:
                tokens_stemmed.append((token,"n"))
            continue
        token_stemmed = token
        is_verb = "n"
        for prefix in verb_prefix:
            for suffix in verb_suffix:
                if len(token) - len(prefix) - len(suffix) > 2 and token[: len(prefix)] == prefix and token[len(token) - len(suffix) : ] == suffix:
                    token_possible_stem = token[len(prefix) : len(token) - len(suffix) ]
                    if token_possible_stem in verbs and len(token_possible_stem) <= len(token_stemmed):
                        token_stemmed = token_possible_stem
                        if prefix in ['فن','فت','في','ن','ت','ي']:
                            is_verb = "vPresent"
                        elif prefix in ['فا','ا']:
                            is_verb = "vOrder"
                        elif prefix in ['فسن','فست','فسي','سي','ست','سن','سا','فس','س']:
                            is_verb = "vFuture"
                        else:
                            is_verb = "v"
        tokens_stemmed.append((token_stemmed,is_verb))
                        
    return tokens_stemmed