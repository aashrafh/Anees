from collections import Counter
import tokenization
import preprocess
import ner
import verb_extraction
import stemming
import sentimental_analysis
import intent_classifier
import time_extract
import content_extract

def NLU(text):
    #Preprocessing
    text = preprocess.pre_process(text)
    #Tokenization
    tokens = tokenization.get_tokens(text)
    # NER
    ents = ner.get_ents(tokens)
    #Part of Speech and Stemming
    tokens_verb_noun = verb_extraction.extract_stem_verb(tokens,ents)
    tokens_verb_noun = stemming.stem(tokens_verb_noun)
    return text , emotion , tokens ,ents , tokens_verb_noun


if __name__ == "__main__":
    spoken = 0
    emotion_list = list()
    use_emotion = False
    emotion_to_be_used = 'neutral'
    while(True):
        text = input()
        spoken += 1
        #Sentimental Analysis
        emotion = sentimental_analysis.get_emotion(text)
        emotion_list.append(emotion)
        if spoken == 3:
            #use the majority emotion in list to answer using it
            c = Counter(emotion_list)
            use_emotion = True
            emotion_to_be_used = c.most_common(1)
            if dict(c)[emotion_to_be_used] == 1:
                emotion_to_be_used = 'neutral'
        #check if category location(parmacy,libirary) of user is repeated for a number of time then use the recommendation
        # if category == same category:
        #   use recommendation system of maps
        # Task
        intent = intent_classifier.intent(text)
        if intent == 'general' or intent == 'greeting' or intent == 'thank':
            #call generation api
            pass
        else:
            text , tokens ,ents , tokens_verb_noun = NLU(text)
            #use Question or Not intent
            #extract Time
            match   intent:
                case 'weather':
                    #use Q or not intent if its not Q then call customized weather with generation api 
                    #call weather model
                    pass
                case 'schedule':
                    edited_time, tokens_used, filtered_tokens = time_extract(tokens, tokens_verb_noun)
                    content = content_extract(text, tokens_used, filtered_tokens)
                    print (edited_time, content)
                    pass
                case 'recommendation':
                    #call recommendation model
                    pass
                case 'sports':
                    #call sports generation model
                    pass
                case default:
                    #call generation(Search) api
                    pass
        use_emotion = False
        spoken = 0
        emotion_to_be_used = 'neutral'
        emotion_list = list()
    

    
    
    


