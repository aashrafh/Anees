from calendar import month
from datetime import datetime
from threading import currentThread
from dateutil.relativedelta import relativedelta
#-----------------------------------------
def edit_distance (word1, word2,):
    index1 = len(word1)
    index2 = len(word2)
    dp = [[0 for x in range(index2 + 1)] for x in range(index1 + 1)]
    for i in range (index1 + 1):
        for j in range (index2 + 1):
            if i == 0:
                dp[i][j] == j
            elif j == 0:
                dp[i][j] == i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                 dp[i][j] = 1 + min ( dp[i-1][j-1], #replace
                                    dp[i-1][j],     #remove
                                    dp[i][j-1])     #insert
    return dp[index1][index2]
#-------------------------------------------------------------------------
def get_closest_number (word):
    numbersBagOfWords = numbers_bag_of_words()
    if word.isnumeric():
        return int(word), 0
    number_index, editDistance = get_closest_word_with_threshold(word, numbersBagOfWords) 
    return number_index + 1, editDistance
#------------------------------------------------------------------------
def get_closest_month (word):
    monthsBagOfWords = ["يناير","فبراير","مارس","ابريل","مايو","يونيو","يوليو","اغسطس","سبتمبر","اكتوبر","نوفمبر","ديسمبر"]
    month_index, _ = get_closest_word_with_threshold(word, monthsBagOfWords)
    if month_index == -1:
        return 0
    current_month = datetime.now().month - 1
    if month_index - current_month > 0:
        return month_index - current_month
    return 12 - (current_month - month_index) 
#------------------------------------------------------------------------
def get_closest_day(word):
    daysBagOfWords = ["اتنين","تلات","اربع","خميس","جمعه","سبت","احد"]
    day_index, _ =  get_closest_word_with_threshold(word, daysBagOfWords) 
    if day_index == -1:
        return 0
    current_day = datetime.now().weekday()
    if day_index - current_day > 0:
        return day_index - current_day
    return 7 - (current_day - day_index)
#------------------------------------------------------------------------
def get_closest_hour(dummy):
    return 0
#------------------------------------------------------------------------
def get_closest_word_with_threshold (word, bag_of_words, threshold = 0.35):
    editDistance = 1
    closest_word_index = 0
    closest_word = bag_of_words[0]
    for index, token in enumerate(bag_of_words):
        editDistanceRatio = edit_distance(word, token)  / min(len(token), len(word))
        if (editDistanceRatio < editDistance or 
        (editDistanceRatio == editDistance and abs( len(token) - len(word)) < abs( len(closest_word) - len(word)))):
            editDistance = editDistanceRatio
            closest_word = token
            closest_word_index = index
    if editDistance > threshold:
        return -1, 1000 # not included in the bag of word
    return closest_word_index, editDistance
#------------------------------------------------------------------------    
def bigrams (tokens):
    grams = []
    for index in range(len(tokens) - 1):
        grams.append([tokens[index] , tokens[index + 1]])
    return grams
#------------------------------------------------------------------------
def numbers_bag_of_words():
    singleNumbers = ["واحد","اتنان","تلاته","اربعه","خمسه","سته","سبعه","تمانيه","تسعه"]
    higherNumbers = ["عشر","عشرين","تلاتين","اربعين","خمسين"]
    numbersBagOfWords = []
    for number in singleNumbers:
        numbersBagOfWords.append(number)    

    for higher in higherNumbers:
        if higher == "عشر":
            numbersBagOfWords.append(higher + "ه")
        else:
            numbersBagOfWords.append(higher)
        for number in singleNumbers:
            if higher == "عشر" or higher == "":
                numbersBagOfWords.append(number + higher)    
            else:
                numbersBagOfWords.append(number + "و" + higher)
    return numbersBagOfWords
#------------------------------------------------------------------------
def get_time(tokens, task):
    # اسابيع ناقصة

    bigram = bigrams(tokens)
    bigram.reverse()
    # minuteEdit, hourEdit, dayEdit, monthEdit, overwriteHour, overwriteDay, overwriteMonth, at night
    edits = [0, 0, 0, 0, 0, 0, 0, 1]
    # incremental specifiers -> [check index in edits, how much to add]
    time_specifiers_increment = {
        "ساعه" : [1, 1], "يوم" : [2, 1], "شهر" : [3, 1], "اسبوع" : [2, 7],
        "ساعتين" : [1, 2], "يومين" : [2, 2], "شهرين" : [3, 2], "اسبوعين" : [2, 14],
        "ساعات" : [1, 3], "ايام" : [2, 3], "شهور" : [3, 3],"اسابيع" : [2, 9],
        "ربع" : [0, 15], "تلت" : [0, 20], "نص" : [0, 30],
        "دقايق" : [0, 3], "دقيقه" : [0, 3],
    }
    # set specifiers -> [chech index in edits, how much to set]
    time_specifiers_set = {
        "ساعه" : [1], "يوم" : [2], "شهر" : [3]
    }
    bagOfWordsFunctions = [get_closest_hour, get_closest_day, get_closest_month]
    tokens_used = [0] * len(tokens)
    for index, gram in enumerate(bigram):
        if gram[0] in time_specifiers_set :
            specifier = time_specifiers_set.get(gram[0])
            if edits[specifier[0]] == 0 and tokens_used[tokens.index(gram[0])] == 0 and tokens_used[tokens.index(gram[1])] == 0:
                edits[specifier[0]], _ = get_closest_number(gram[1])
                if edits[specifier[0]] != 0: # "شهر 12","يوم 22","الساعة 4"
                    edits[specifier[0] + 3] = 1
                    tokens_used[tokens.index(gram[0])] = 1
                    tokens_used[tokens.index(gram[1])] = 1
                else:  # "شهر يناير","يوم الجمعة"
                    edits[specifier[0]] = bagOfWordsFunctions[specifier[0] - 1](gram[1])
                    if edits[specifier[0]] != 0:
                        tokens_used[tokens.index(gram[0])] = 1
                        tokens_used[tokens.index(gram[1])] = 1
        
        if gram[1] in time_specifiers_increment:
            specifier = time_specifiers_increment.get(gram[1])
            if edits[specifier[0]] == 0 and tokens_used[tokens.index(gram[1])] == 0 :
                edits[specifier[0]] = specifier[1]
                if specifier[1] == 1 or specifier[1] == 7 and tokens_used[tokens.index(gram[0])] == 0:
                    number, _ = get_closest_number(gram[0])
                    edits[specifier[0]] = specifier[1] * number # mode to handle weeks (7 * days)
                    tokens_used[tokens.index(gram[0])] = 1

                elif specifier[1] >= 3 and specifier[1] <= 9 and tokens_used[tokens.index(gram[0])] == 0: # ايام شهور اسابيع ساعات
                    number, _ = get_closest_number(gram[0])
                    edits[specifier[0]] = (specifier[1] - 2) * number # mode to handle weeks (7 * days)
                    tokens_used[tokens.index(gram[0])] = 1
                tokens_used[tokens.index(gram[1])] = 1
    # no specifiers
    if edits[1] == 0 and task == 'schedule':     
        minDistance = 1000
        token_index = -1
        for index, token in enumerate(tokens):
            if tokens_used[index] == 0:
                hoursEdit, distance = get_closest_number(token)
                if hoursEdit != 0 and distance < minDistance:
                    minDistance = distance
                    edits[1] = hoursEdit
                    edits[4] = 1
                    token_index = index
        if token_index != -1:
            tokens_used[token_index] = 1

    time_specifiers_tokens = {
        "صبح" : [0, 7], "ليل" : [1, 8], "صباح" : [0, 7], "نهار" : [1, 12], "ظهر" : [1, 12], "عصر" : [1, 3], "مغرب" : [1, 6] ,
        "عشاء" : [1, 8], "عشا" : [1, 8], "فجر" : [0, 3]
    }
    for token in tokens:
        if token == "بكره":
            edits[2] = 1
        elif token in time_specifiers_tokens:
            tokens_used[tokens.index(token)] = 1
            edits[7] = time_specifiers_tokens.get(token)[0]   
            if edits[1] == 0:
                edits[1] = time_specifiers_tokens.get(token)[1]
                edits[4] = 1   

    if edits[1] >= 12:
        edits[1] = 11
    return edits, tokens_used
# need to add "الا ربع" "الا تلت" 
# 1 minor issue the code cannot differentiate between (2, الاتنين) (3, التلات) and so on
# it is a static code any error will result into a disaster XD
#---------------------------------------------------------------------------
def edit_time (edits):
    now_time = datetime.now()
    # create new time with the overwrite values
    new_time = datetime(year= now_time.year
                        , month= ( edits[3] * edits[6] ) + ( now_time.month * (not edits[6]) )
                        , day=   ( edits[2] * edits[5] ) + ( now_time.day * (not edits[5]) )
                        , hour=  ( edits[1]+ 12 * edits[7]) * edits[4]  + ( now_time.hour * (not edits[4]) )
                        , minute=( edits[0] * edits[4] ) + ( now_time.minute * (not edits[4]) ))
    # add the incremental values
    new_time = new_time + relativedelta(minutes= edits[0] * (not edits[4]), hours=edits[1] * (not edits[4]), days=edits[2] * (not edits[5]), months=edits[3] * (not edits[6]))
    if new_time <= now_time:
        new_time = new_time + relativedelta(minutes=1)
    if new_time <= now_time:
        new_time = new_time - relativedelta(minutes=1) + relativedelta(hours=1)
    if new_time <= now_time:
        new_time = new_time - relativedelta(minutes=1) - relativedelta(hours=1) + relativedelta(days=1)
    if new_time <= now_time:
        new_time = new_time - relativedelta(minutes=1) - relativedelta(hours=1) - relativedelta(days=1) + relativedelta(months=1)
    if new_time <= now_time:
        new_time = new_time - relativedelta(minutes=1) - relativedelta(hours=1) - relativedelta(days=1) - relativedelta(months=1) + relativedelta(years=1) 
    return new_time

#------------------------------------------------------------------------
def main(tokens, tokens_verb_noun , task = 'schedule'):
    filtered_tokens = []
    for index, token in enumerate(tokens):
        if tokens_verb_noun[index][1] != "vOrder":
            filtered_tokens.append(token)
    for index, token in enumerate(filtered_tokens):
        if token[0] == 'ا' and token[1] == 'ل':
            filtered_tokens[index] = token[2:]
        elif token[0] == 'و' :
            filtered_tokens[index] = token[1:]
    edit, tokens_used = get_time(filtered_tokens, task)
    edited_time = edit_time(edit)
    return edited_time, tokens_used, filtered_tokens

