from datetime import datetime
from dateutil.relativedelta import relativedelta
#-----------------------------------------
def edit_distance (word1, word2, index1, index2):
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
def textNumberToNumber(word,numbersBagOfWords):
    if word.isnumeric():
        return int(word), 0
    editDistance = 1000
    closestNumber = "واحد"
    for index, number in enumerate(numbersBagOfWords):
        editDistanceNew = edit_distance(word, number, len(word), len(number))
        if (editDistanceNew < editDistance or 
        (editDistanceNew == editDistance and abs( len(number) - len(word)) < abs( len(closestTextualNumber) - len(word)))):
            editDistance = editDistanceNew
            closestTextualNumber = number
            closestNumber = index + 1
    print(closestNumber)
    if editDistance >= 3:
        return 0, editDistance
    return closestNumber, editDistance
#------------------------------------------------------------------------    
def bigrams (tokens):
    grams = []
    for index in range(len(tokens) - 1):
        grams.append([tokens[index] , tokens[index + 1]])
    return grams
#------------------------------------------------------------------------
def numbers_bag_of_words():
    singleNumbers = ["واحد","اتنين ","تلاته","اربعه","خمسه","سته","سبعه","تمانيه","تسعه"]
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
    # اسبوع ناقصة
    numbersBagOfWords = numbers_bag_of_words()
    bigram = bigrams(tokens)
    bigram.reverse()
    # minuteEdit, hourEdit, dayEdit, monthEdit, overwriteHour, overwriteDay, overwriteMonth, at night
    edits = [0, 0, 0, 0, 0, 0, 0, 1]
    # specifier -> [check index in edits, how much to add]
    time_specifiers_second = {
        "ساعه" : [1, 1], "يوم" : [2, 1], "شهر" : [3, 1], "بكره" : [2, 1],
        "ساعتين" : [1, 2], "يومين" : [2, 2], "شهرين" : [3, 2],
        "ساعات" : [1, 3], "ايام" : [2, 3], "شهور" : [3, 3],
        "ربع" : [0, 15], "تلت" : [0, 20], "نص" : [0, 30],
        "دقايق" : [0, 3], "دقيقه" : [0, 3]
    }
    time_specifiers_first = {
        "ساعه" : [1], "يوم" : [2], "شهر" : [3]
    }
    tokens_used = [0] * len(tokens)
    for index, gram in enumerate(bigram):
        if gram[0] in time_specifiers_first :
            specifier = time_specifiers_first.get(gram[0])
            if edits[specifier[0]] == 0:
                edits[specifier[0]], _ = textNumberToNumber(gram[1], numbersBagOfWords)
                edits[specifier[0] + 3] = 1
                
                tokens_used[tokens.index(gram[0])] = 1
                tokens_used[tokens.index(gram[1])] = 1
        
        if gram[1] in time_specifiers_second:
            specifier = time_specifiers_second.get(gram[1])
            if edits[specifier[0]] == 0:
                edits[specifier[0]] = specifier[1]
                if specifier[1] == 3:
                    edits[specifier[0]], _ = textNumberToNumber(gram[0], numbersBagOfWords) 
                    tokens_used[tokens.index(gram[0])] = 1
                tokens_used[tokens.index(gram[1])] = 1

    # no specifiers
    if edits[1] == 0 and task == 'schedule':            
        minDistance = 1000
        token_index = -1
        for index, token in enumerate(tokens):
            if tokens_used[index] == 0:
                hoursEdit, distance = textNumberToNumber(token, numbersBagOfWords)
                if hoursEdit != 0 and distance < minDistance:
                    minDistance = distance
                    edits[1] = hoursEdit
                    edits[4] = 1
                    token_index = index
        if token_index != -1:
            tokens_used[token_index] = 1

    time_specifiers_tokens = {
        "صبح" : [0], "ليل" : [1], "صباح" : [0], "نهار" : [1], "ظهر" : [1], "عصر" : [1], "مغرب" : [1] ,
        "عشاء" : [1], "عشا" : [1], "فجر" : [0]
    }
    for token in tokens:
        if token in time_specifiers_tokens:
            tokens_used[tokens.index(token)] = 1
            edits[7] = time_specifiers_tokens.get(token)[0]   
    if edits[1] > 23 and edits[4] == 1:
        edits[1] = 23
    return edits, tokens_used
# need to add "الصبح" "بليل" 
# need to add "الا ربع" "الا تلت" 
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

