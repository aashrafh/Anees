import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tokenization
import preprocess
import ner
import verb_extraction
import stemming
import sentimental_analysis
import intent_classifier
import time_extract
import content_extract
import weather
import recomm_intent
import dill
import pos
import pickle
from tensorflow import keras
import numpy as np

def get_models():
    def stopwords_extraction():
        file = open("../Data/stopwords.txt","r",encoding="utf-8")
        stopwords = file.read().split()
        file.close()
        return stopwords
    def get_ner_instance():
        with open("../utils/ner_instance", 'rb') as in_strm:
            ner_instance = dill.load(in_strm)
        return ner_instance

    def verb_dictionary():
        file = open("../Data/verb_dictionary.txt","r",encoding="utf-8")
        verbs = file.read().split()
        file.close()
        return verbs

    def nouns_extract():
        file = open("../Data/noun_dictionary.txt","r",encoding="utf-8")
        nouns = file.read().split()
        file.close()
        return nouns

    def get_emotion_models():
        filename = f'Sentimental_Analysis/models/sentmental_all_model.sav'
        model = pickle.load(open(filename, 'rb'))
        filename = f'Sentimental_Analysis/models/tfidf_all_model.sav'
        tf_idf = pickle.load(open(filename, 'rb'))
        return model, tf_idf

    def get_intent_models():
        m = keras.models.load_model("Intent_Classification/models")
        filename = f'../utils/tokenizer.sav'
        tokenizer = pickle.load(open(filename, 'rb'))
        return m,tokenizer

    def get_recomm_intent_models():
        m = keras.models.load_model("Recommendation_intent/intent/movie_location_model")
        filename = f'../utils/recomm_tokenizer.sav'
        tokenizer = pickle.load(open(filename, 'rb'))
        return m,tokenizer

    def get_location_recomm_model():
        with open("../utils/location_recommender", 'rb') as in_strm:
            location_recomm = dill.load(in_strm)
        return location_recomm

    def get_movie_recomm_model():
        with open("../utils/movie_recommender", 'rb') as in_strm:
            movie_recomm = dill.load(in_strm)
        return movie_recomm
    stopwords = stopwords_extraction()
    ner_instance = get_ner_instance()
    verbs = verb_dictionary()
    nouns = nouns_extract()
    emotions_model , emotions_tf_idf = get_emotion_models()
    intent_model,tokenizer = get_intent_models()
    recomm_intent_model,recomm_tokenizer = get_recomm_intent_models()
    location_recomm = get_location_recomm_model()
    movie_recomm = get_movie_recomm_model()
    return stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,location_recomm,movie_recomm

def NLU(text,stopwords,ner_instance,verbs,nouns):
    #Preprocessing
    text = preprocess.pre_process(text)
    #Tokenization
    tokens = tokenization.get_tokens(text,stopwords)
    # NER
    ents = ner.get_ents(tokens,ner_instance)
    #Part of Speech and Stemming
    part_of_speech = pos.part_of_speech(tokens,nouns,ents)
    tokens_verb_noun = verb_extraction.extract_stem_verb(tokens,verbs,part_of_speech,ents)
    tokens_verb_noun = stemming.stem(tokens_verb_noun)
    return text , tokens ,ents , tokens_verb_noun


def main(text,stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,location_recomm,movie_recomm):
    
    #Start of chat
    response = dict()
    text , tokens ,ents , tokens_verb_noun = NLU(text,stopwords,ner_instance,verbs,nouns)
    preprocessed_text = " ".join(tokens) 
    #Sentimental Analysis
    emotion = sentimental_analysis.get_emotion(preprocessed_text,emotions_model , emotions_tf_idf)
    # Tasks
    intent = intent_classifier.intent(preprocessed_text,intent_model,tokenizer)
    print(intent)
    if intent == 'general' or intent == 'greeting' or intent == 'thank':
        #call generation api
        response["message"] = "انتا يلا من اسيوط"
    else:
        match   intent:
            case 'weather':
                response["message"] = weather.main(tokens,tokens_verb_noun,ents)
            case "schedule":
                edited_time, tokens_used, filtered_tokens = time_extract.main(tokens, tokens_verb_noun)
                content = content_extract.get_schedule_content(text, tokens_used, filtered_tokens)
                response["edited_time"] = edited_time
                response["content"] = content
            case 'recommendation':
                r_intent = recomm_intent.intent(preprocessed_text,recomm_intent_model,recomm_tokenizer)
                print(r_intent)
                if r_intent == 'movies':
                    movie, categories = content_extract.get_movies_content(text, tokens, tokens_verb_noun)
                    print (movie, categories)
                    if movie != "" and len(categories) != 0:
                        pass
                    elif movie != "":
                        response["movies"] = movie_recomm.general_recommendation(movie_recomm.get_movie_id(movie)[0])["similar_movies"][:3]
                    elif len(categories) != 0:
                        categories = np.array(categories)
                        response["movies"] = movie_recomm.recommend_given_categories(categories[:,0])
                    else:
                        pass
                    intent = "recommendation-movies"
                else :
                    location_data = location_recomm.search_by_text(preprocessed_text)
                    locations = list()
                    for loc in location_data[:3]:
                        locations.append({"الاسم":loc["name"],"تقييم المكان ":loc["rating"],"العنوان":loc["formatted_address"]})
                    response["places"] = locations
                    intent = "recommendation-places"
            case default:
                #call generation(Search) api
                pass
    return intent, emotion, response
        
# stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,location_recomm,movie_recomm = get_models()
# print(main("اقترح فيلم كوميدى جديد لاشاهده",stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,location_recomm,movie_recomm))