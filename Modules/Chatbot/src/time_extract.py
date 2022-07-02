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
#------------------------------------------------------------------------
def textNumberToNumber(word,numbersBagOfWords):
    if word.isnumeric():
        return int(word)
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
        return 0
    return closestNumber
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
def get_time(tokens):
    numbersBagOfWords = numbers_bag_of_words()
    overwriteHour, overwriteDay, overwriteMonth, morning, minuteEdit, hourEdit, dayEdit, monthEdit = 0, 0, 0, 0, 0, -2, 0, 0
    bigram = bigrams(tokens)
    bigram.reverse()
    for gram in bigram:

        if gram[1] == "ربع" and gram[0] == "الا" and minuteEdit == 0:
            hourEdit -= 1
            minuteEdit = 45
        elif (gram[0] == "ربع" or gram[0] == "وربع") and minuteEdit == 0:
            minuteEdit = 15
        if gram[1] == "تلت" and gram[0] == "الا" and minuteEdit == 0:
            hourEdit -= 1
            minuteEdit = 40
        elif (gram[0] == "تلت" or gram[0] == "وتلت") and minuteEdit == 0:
            minuteEdit = 20
        elif (gram[0] == "نص" or gram[0] == "ونص") and minuteEdit == 0:
            minuteEdit = 30
        elif (gram[1] == "دقيقه" or gram[1] == "دقايق")and minuteEdit == 0:
            minuteEdit = textNumberToNumber(gram[0],numbersBagOfWords)

        if gram[0] == "ساعه" and hourEdit <= -2: 
            hourEdit += textNumberToNumber(gram[1],numbersBagOfWords) + 2
            overwriteHour = 1
        elif gram[1] == "ساعه" and hourEdit <= -2:
            hourEdit += 3
        elif gram[1] == "ساعتين" and hourEdit <= -2:
            hourEdit += 4
        elif gram[1] == "ساعات" and hourEdit <= -2:
            hourEdit += textNumberToNumber(gram[0],numbersBagOfWords) + 2

        if gram[0] == "يوم" and dayEdit == 0: 
            dayEdit = textNumberToNumber(gram[1],numbersBagOfWords) 
            overwriteDay = 1
        elif gram[1] == "يوم" and dayEdit == 0:
            dayEdit = 1
        elif gram[1] == "يومين" and dayEdit == 0:
            dayEdit = 2
        elif gram[1] == "ايام" and dayEdit == 0:
            dayEdit = textNumberToNumber(gram[0],numbersBagOfWords) 

        if gram[0] == "شهر" and monthEdit == 0: 
            monthEdit = textNumberToNumber(gram[1],numbersBagOfWords) 
            overwriteMonth = 1
        elif gram[1] == "شهر" and monthEdit == 0:
            monthEdit = 1
        elif gram[1] == "شهرين" and monthEdit == 0:
            monthEdit = 2
        elif gram[1] == "شهور" and monthEdit == 0:
            monthEdit = textNumberToNumber(gram[0],numbersBagOfWords) 
        
    return minuteEdit ,hourEdit, dayEdit, monthEdit, overwriteHour, overwriteDay, overwriteMonth


# number without specifications should be an hour
# need to add "بكرة" "بعد بكرة" "الصبح" "بليل" 
# cannot deiffrentiate between "watch" and "hour" both are "ساعة"
# need to optimize the code 
# it is a static code any error will result into a distaster XD
#------------------------------------------------------------------------
def main(tokens):
    for index, token in enumerate(tokens):
        if token[0] == 'ا' and token[1] == 'ل':
            tokens[index] = token[2:]
    minuteEdit ,hourEdit, dayEdit, monthEdit, overwriteHour, overwriteDay, overwriteMonth = get_time(tokens)
    return minuteEdit ,hourEdit, dayEdit, monthEdit, overwriteHour, overwriteDay, overwriteMonth

