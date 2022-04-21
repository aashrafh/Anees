verb_prefix = {'فسن','فست','فسي','فا','سي','ست','سن','سا','فن','فت','في','فس','س','ف','ن','ت','ي','ا'}
verb_suffix = {'ى','تما','ا','ت','ين','ان','و','وا','تن','تم','تا','نا','ون','ن'}
def verb_dictionary():
    file = open("../Data/verb_dictionary.txt","r",encoding="utf-8")
    verbs = file.read().split()
    file.close()
    return verbs
def extract_stemm_verb(tokens):
    verbs = verb_dictionary()
    result = list()
    for token in tokens:
        len_token = len(token)
        if len_token < 4:
            if token in verb_dictionary:
                result.append((token,"v"))
            else:
                result.append((token,"nv"))
            continue
#(-,verb,notverb)