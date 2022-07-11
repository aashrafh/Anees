def part_of_speech(tokens,nouns,ents):
    result = list()
    for token in tokens:
        if token in ents.keys():
            result.append((token,ents[token]))
        elif token in nouns:
            result.append((token,'n'))
        else:
            result.append((token,'v'))
    return result