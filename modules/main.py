from re import search
import numpy as np
from tensorflow import keras
import pickle
import pos
import dill
import recomm_intent
import weather
import content_extract
import time_extract
import intent_classifier
import sentimental_analysis
import stemming
import verb_extraction
import ner
import preprocess
import tokenization
import q_not
import search
from config import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def get_models():
    def stopwords_extraction():
        file = open(STOPWORDS_PATH, "r", encoding="utf-8")
        stopwords = file.read().split()
        file.close()
        return stopwords

    def get_ner_instance():
        ner_instance = pickle.load(open(NER_PATH, 'rb'))
        return ner_instance

    def verb_dictionary():
        file = open(VERB_DICTIONAY_PATH, "r", encoding="utf-8")
        verbs = file.read().split()
        file.close()
        return verbs

    def nouns_extract():
        file = open(NOUN_DICTIONAY_PATH, "r", encoding="utf-8")
        nouns = file.read().split()
        file.close()
        return nouns

    def get_emotion_models():
        model = pickle.load(open(SENTIMENTAL_MODEL_PATH, 'rb'))
        tf_idf = pickle.load(open(TFIDF_MODEL_PATH, 'rb'))
        return model, tf_idf

    def get_Q_not_models():
        model = pickle.load(open(Q_NOT_MODEL_PATH, 'rb'))
        tf_idf = pickle.load(open(TFIDF_Q_NOT_MODEL_PATH, 'rb'))
        return model, tf_idf

    def get_intent_models():
        m = keras.models.load_model(INTENT_CLASSIFICATION_MODEL_PATH)
        tokenizer = pickle.load(open(TOKENIZER_MODEL_PATH, 'rb'))
        return m, tokenizer

    def get_recomm_intent_models():
        m = keras.models.load_model(MOVIE_LOCATION_MODEL_PATH)
        tokenizer = pickle.load(open(RECOMM_TOKENIZER_MODEL_PATH, 'rb'))
        return m, tokenizer

    def get_location_recomm_model():
        with open(LOCATION_RECOMMENDER_MODEL_PATH, 'rb') as in_strm:
            location_recomm = dill.load(in_strm)
        return location_recomm

    def get_movie_recomm_model():
        with open(MOVIE_RECOMMENDER_MODEL_PATH, 'rb') as in_strm:
            movie_recomm = dill.load(in_strm)

        return movie_recomm
    stopwords = stopwords_extraction()
    ner_instance = get_ner_instance()
    verbs = verb_dictionary()
    nouns = nouns_extract()
    emotions_model, emotions_tf_idf = get_emotion_models()
    intent_model, tokenizer = get_intent_models()
    recomm_intent_model, recomm_tokenizer = get_recomm_intent_models()
    location_recomm = get_location_recomm_model()
    movie_recomm = get_movie_recomm_model()
    q_not_model, tf_idf_q_not = get_Q_not_models()
    return stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer, recomm_intent_model, recomm_tokenizer, location_recomm, movie_recomm, q_not_model, tf_idf_q_not


def NLU(text, stopwords, ner_instance, verbs, nouns):
    # Preprocessing
    text = preprocess.pre_process(text)
    # Tokenization
    tokens = tokenization.get_tokens(text, stopwords)
    # NER
    ents = ner.get_ents(tokens, ner_instance)
    # Part of Speech and Stemming
    part_of_speech = pos.part_of_speech(tokens, nouns, ents)
    tokens_verb_noun = verb_extraction.extract_stem_verb(
        tokens, verbs, part_of_speech, ents)
    tokens_verb_noun = stemming.stem(tokens_verb_noun)
    return text, tokens, ents, tokens_verb_noun


def search_module(text, q_not_model, tf_idf_q_not, ents, tokens_verb_noun):
    response = dict()
    intent = "general"
    question = q_not.get_q_not(text, q_not_model, tf_idf_q_not)
    if (question == 'Q' and 'B-ORG' in ents.values()) or content_extract.get_search(tokens_verb_noun) == 1:
        intent = 'search'
        response['text'] = search.search(text)
    return response, intent


def main(text, location, stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer, recomm_intent_model, recomm_tokenizer, q_not_model, tf_idf_q_not):
    # Start of chat
    response = dict()
    text, tokens, ents, tokens_verb_noun = NLU(
        text, stopwords, ner_instance, verbs, nouns)
    preprocessed_text = " ".join(tokens)
    # Sentimental Analysis
    emotion = sentimental_analysis.get_emotion(
        preprocessed_text, emotions_model, emotions_tf_idf)
    # Tasks
    intent = intent_classifier.intent(
        preprocessed_text, intent_model, tokenizer)
    match   intent:
        case 'general':
            response, intent = search_module(
                text, q_not_model, tf_idf_q_not, ents, tokens_verb_noun)
        case 'weather':
            print("calling the weather module...")
            response["text"] = weather.main(
                tokens, tokens_verb_noun, ents, location)

        case "schedule":
            print("calling the schedule module...")
            edited_time, tokens_used, filtered_tokens = time_extract.main(
                tokens, tokens_verb_noun)
            content = content_extract.get_schedule_content(
                text, tokens_used, filtered_tokens)
            response["edited_time"] = edited_time
            response["content"] = content
            response['text'] = "انا حجزتلك معاد فالنتيجة\n\n" + "بعنوان : " + response["content"] + \
                "\n\nوميعاد : " + \
                response['edited_time'].strftime("%m/%d/%Y, %H:%M:%S") + "\n"

        case 'recommendation':
            print("calling the recommendation intent module...")
            r_intent = recomm_intent.intent(
                preprocessed_text, recomm_intent_model, recomm_tokenizer)

            if r_intent == 'movies':
                intent = "recommendation-movies"
                movie, categories = content_extract.get_movies_content(
                    text, tokens, tokens_verb_noun)
                categories = np.array(categories)
                if movie == "" and len(categories) == 0:
                    response, intent = search_module(
                        text, q_not_model, tf_idf_q_not, ents, tokens_verb_noun)
                else:
                    response["movie"] = movie
                    response["categories"] = categories
            else:
                intent = "recommendation-places"
                response["places"] = preprocessed_text
    return intent, emotion, response

#stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer, recomm_intent_model, recomm_tokenizer, location_recomm, movie_recomm,q_not_model , tf_idf_q_not = get_models()
#print(main("من قام ب انشاء الاهلى ؟",stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,q_not_model , tf_idf_q_not))
