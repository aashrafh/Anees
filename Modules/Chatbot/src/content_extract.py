from time_extract import edit_distance, get_closest_word_with_threshold
import re
import pandas as pd
def get_closest_word (word, tokens):
    min_dist = 10000
    min_index = 0
    for index, wordInText in enumerate(tokens):
        distance = edit_distance(word,wordInText)
        if distance < min_dist:
            min_dist = distance
            min_index = index
    return min_index
#------------------------------------------------------------------------
def get_schedule_content(text, tokens_used, filtered_tokens):
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

    text_splitted = text.split()
    content = text_splitted[ get_closest_word (filtered_tokens[longest_subsequence_start], text_splitted):
    get_closest_word (filtered_tokens[ longest_subsequence_start + longest_subsequence - 1], text_splitted) + 1]
    content = " ".join(content)
    return content
#-------------------------------------------------------------------------------------
def get_movie (text):
    return text.split('(')[0].lower().strip()
def get_movies_content (text, tokens, tokens_verb_noun):
    movies_bag_of_words_eng = ['action','adventure','animation','children','comedy','crime','documentary','drama','fantasy','horror','musical','mystery','romance','sci-fi','war','western']
    movies_bag_of_words_ar = ['اكشن','مغامره','انيميشن','اطفال','كوميدي','جريمه','وثايقي','دراما','خيال','رعب','موسيقي','غموض','رومانسي','علمي','حروب','ويستيرن']
    categories = []
    movie = re.findall("[a-zA-Z]*", text) 
    movie = " ".join(movie)
    movie = re.sub(' +', ' ',movie).lower().strip()
    df = pd.read_csv("Task_data/movies.csv")
    movies = df["title"].apply(func=get_movie)
    if movie not in list(movies):
        movie = ""
    for index, word in enumerate(tokens):
        if tokens_verb_noun[index][1] == 'n':
            index, distance = get_closest_word_with_threshold(word,movies_bag_of_words_ar, 0.4)
            if index != -1:
                categories.append([movies_bag_of_words_eng[index], 1 - distance])
    return movie, categories
#-------------------------------------------------------------------------------------
def get_places_content ():
    place = ""
    categories = [] 
    return place, categories



