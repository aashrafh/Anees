def nouns_extract():
    file = open("../Data/noun_dictionary.txt","r",encoding="utf-8")
    nouns = file.read().split()
    file.close()
    return nouns
def part_of_speech(tokens):
    nouns = nouns_extract()
    result = list()
    for token in tokens:
        if token in nouns:
            result.append((token,'n'))
        else:
            result.append((token,'v'))
    return result