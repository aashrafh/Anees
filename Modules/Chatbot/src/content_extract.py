from time_extract import edit_distance
def get_closest_word (word, tokens):
    min_dist = 10000
    min_index = 0
    for index, wordInText in enumerate(tokens):
        distance = edit_distance(word,wordInText, len(word), len(wordInText))
        if distance < min_dist:
            min_dist = distance
            min_index = index
    return min_index
#------------------------------------------------------------------------

def main(text, tokens_used, filtered_tokens):
    longest_subsequence, longest_subsequence_start, start_index, last_index = -1, 0, 0, 0
    for index, used_token in enumerate(tokens_used):
        if used_token == 0:
            last_index += 1
        else:
            if last_index - start_index > longest_subsequence :
                longest_subsequence = last_index - start_index
                longest_subsequence_start = start_index
            start_index, last_index =  index + 1, index + 1
    if used_token == 0:
        if last_index - start_index > longest_subsequence :
                longest_subsequence = last_index - start_index
                longest_subsequence_start = start_index
            
    filtered_tokens[longest_subsequence_start]
    print (filtered_tokens[longest_subsequence_start], filtered_tokens[ longest_subsequence_start + longest_subsequence - 1])

    text_splitted = text.split()
    content = text_splitted[ get_closest_word (filtered_tokens[longest_subsequence_start], text_splitted):
    get_closest_word (filtered_tokens[ longest_subsequence_start + longest_subsequence - 1], text_splitted) + 1]
    content = " ".join(content)
    return content
