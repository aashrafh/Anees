from urllib import request
from flask import Flask, request, abort, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import warnings
import sys
import os
import requests
from datetime import datetime
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

module_path = os.path.abspath(os.path.join(
    'F:\coullage\Year 4\Anees\Modules\Chatbot\src'))
if module_path not in sys.path:
    sys.path.append(module_path)
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = "mongodb://localhost:27017/Anees"
mongo = PyMongo(app)
usersCollection = mongo.db.users

print("importing the main....")
import main


@app.route('/getResponse', methods=['POST'])
def get_response():
    username = request.json['username']
    username = username.strip()
    text = request.json['text']
    location = request.json['location']
    user = usersCollection.find_one({'username': username})
    if user == None:
         return jsonify(message='اسم المستخدم دة مش موجود !!'), 403
    intent, emotion, response = main.main(text, location, stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer, recomm_intent_model, recomm_tokenizer, q_not_model, tf_idf_q_not)
    print("Intent -> ", intent)
    print("Emotion ->", emotion)
    if intent == 'general':
        messages = user['messages']
        messages = [{"message": message['message'], 'isUser':message['isUser'] } for message in messages if message['isGeneral'] == 1]
        if len(messages) > 4:
            messages = messages[:4]
        messages = messages[::-1]
        response = requests.post(
            'https://4f6d-35-237-130-184.ngrok.io/arz', json={'utter': text, 'history': messages})
        response = response.json()
        response['text'] = response['response']
        

    elif intent == 'recommendation-movies':
        response = movies_recommendation(user, response['movie'], response['categories'], "")

    elif intent == 'recommendation-places':
        response = locations_recommendation(user, response['places'], "", location)

    add_emotion(user, emotion)
    add_location(user, location)
    add_conversation(user, text, 1, intent)
    add_conversation(user, response['text'], 0, intent)
    return {'response': response, 'intent': intent}

# intents ->  recommendation-movies, recommendation-places, schedule, weather, general, *search*, None

@app.route('/schedule_cancel', methods=['PUT'])
def schedule_cancel():
    username = request.json['username']
    username = username.strip()
    user = usersCollection.find_one({'username': username})
    if user == None:
         return jsonify(message='اسم المستخدم دة مش موجود !!'), 403
    text = request.json['text']
    add_conversation(user, text, 0, "schedule", 1)
    return jsonify(message='success'), 200



@app.route('/history', methods=['POST'])
def get_history():
    username = request.json['username']
    username = username.strip()
    user = usersCollection.find_one({'username': username})
    if user == None:
         return jsonify(message='اسم المستخدم دة مش موجود !!'), 403
    history = user['messages']
    return {'response': history, 'intent': 'history'}


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    username = username.strip()
    password = request.json['password']
    user = usersCollection.find_one(
        {'username': username, 'password': password})
    if user == None:
        return jsonify(message= 'اسم المستخدم او كلمة السر غلط'), 403
    return jsonify(message='the user logged in successfully'), 200


@app.route('/signup', methods=['POST'])
def sign_up():
    username = request.json['username']
    username = username.strip()
    password = request.json['password']
    user = usersCollection.find_one({'username': username})
    if user != None:
        return jsonify(message="اسم المستخدم دة حد مستخدمه قبل كدة\nلو سمحت اختار اسم تانى"), 403
    # add all the categories with 0 rating
    all_categories = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
                      'Drama', 'Fantasy', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'War', 'Western']
    movies_categories_liked = []
    for category in all_categories:
        movies_categories_liked.append({'name': category, 'rating': 0})
    usersCollection.insert_one({'username': username, 'password': password,
                                'movies_categories_liked': movies_categories_liked, 'movies': [], 'places': [], 'emotions': ["joy"], 'messages': [], 'locations' : []})
    return jsonify(message='the user is created successfully'), 200


@app.route('/emotions', methods=['POST'])
def get_most_frequent_emotion():
    username = request.json['username']
    username = username.strip()
    user = usersCollection.find_one({'username': username})
    if user == None:
         return jsonify(message='اسم المستخدم دة مش موجود !!'), 403
    emotions = user['emotions']
    # get most frequent emotion using the last 5 messages
    if len(emotions) < 5:
        return {}, "None"
    most_frequent_emotion = max(set(emotions[:5]), key=emotions.count)
    response = {}
    intent = "None"
    if most_frequent_emotion == 'sadness':
        intent = "recommendation-movies"
        response = movies_recommendation(user, "", np.array(
            [['comedy', 1], ['musical', 1]]), "من محادثاتك الاخيرة معايا حسيت انك حزين\n")

    elif most_frequent_emotion == 'anger':
        intent = "recommendation-places"
        locations = user['locations']
        location = {'longitude':locations[0]['longitude'], 'latitude':locations[0]['latitude']}
        print(location)
        response = locations_recommendation(
            user, "عايز اروح مكان هادى", "من محادثاتك الاخيرة معايا حسيت انك متدايق\n", location)

    return {'response': response, 'intent': intent}

@app.route('/update_movie_rating', methods=['PUT'])
def update_movie_rating():
    username = request.json['username']
    username = username.strip()
    movies_rated = request.json['movies']
    user = usersCollection.find_one({'username': username})
    if user == None:
        return jsonify(message='اسم المستخدم دة مش موجود !!'), 403
    for movie_rated in movies_rated:
        movie_name = movie_rated['movie_name']
        rating = movie_rated['rating']
        rating = max(min(rating, 5), 0)
        movies = user['movies']
        genres = user['movies_categories_liked']
        for movie in movies:
            if movie['name'] == movie_name:
                movie['rating'] = rating
                movie_genres = movie['genres'].split('|')
                for genre in genres:
                    if genre['name'] in movie_genres:
                        genre['rating'] = round( (rating + genre['rating']) / 2, 1)
        usersCollection.update_one({'username': username}, {
                                '$set': {'movies': movies, 'movies_categories_liked' : genres}})
    return jsonify(message='success'), 200


def add_emotion(user, emotion):
    username = user['username']
    emotions = user['emotions']
    emotions.insert(0, emotion)
    usersCollection.update_one({'username': username}, {
                               '$set': {'emotions': emotions}})


def add_movie(user, movieName, genres, rating=2.5):
    username = user['username']
    movies = user['movies']
    movie = {'name': movieName, 'rating': rating, 'genres': genres}
    movies.insert(0, movie)
    usersCollection.update_one({'username': username}, {
                               '$set': {'movies': movies}})


def add_place(user, placeName, address, rating=2.5):
    username = user['username']
    places = user['places']
    place = {'name': placeName, 'rating': rating,
             'address': address}
    places.insert(0, place)
    usersCollection.update_one({'username': username}, {
                               '$set': {'places': places}})

def add_location(user, location):
    username = user['username']
    locations = user['locations']
    edit = 0
    for user_location in locations:
        if calculate_distance(user_location['longitude'], user_location['latitude'], location['longitude'], location['latitude']) <= 1:
            user_location['numberOfVisits'] += 1
            edit = 1
    if edit == 0:
        locationDB = {'longitude': location['longitude'], 'latitude': location['latitude'],
                'numberOfVisits': 0}
        locations.insert(0, locationDB)
    usersCollection.update_one({'username': username}, {
                               '$set': {'locations': locations}})

def calculate_distance (lon1, lat1, lon2, lat2):
    R = 6371
    x = (lon2-lon1) * np.cos((lat1+lat2)/2)
    y = (lat2-lat1)
    d = np.sqrt(x*x + y*y) * R
    return d

def add_conversation(user, message, id, intent, removeFirst = 0):
        
    username = user['username']
    messages = user['messages']
    if removeFirst:
        messages.pop(0)
    messageDB = {'isUser':id, 'message': message, 'time': datetime.now(), 'isGeneral' : (1 if intent == "general" else 0)}
    messages.insert(0, messageDB)
    usersCollection.update_one({'username': username}, {
                               '$set': {'messages': messages}})


def send_recommendation(text, type, contents):
    if type == "movies":
        text += "جبتلك فيلمين اهو اتمنى يعجبوك\n\n"
        text += contents[0] + "\n\n"
        text += contents[1] + "\n\n"
        text += "\nوكمان شوية هبعتلك رسالة تقولى رأيك فيهم لو كونت شوفتهم"
    else:
        text += "جبتلك مكانين اهو اتمنى يعجبوك\n\n"
        for content in contents:
            text += "الاسم : " + content['الاسم'] + "\n"
            text += "العنوان : " + content['العنوان'] + "\n\n"
    return text


def movies_recommendation(user, movie, categories, text):
    print("calling the movies module...")
    categories_liked = user['movies_categories_liked']
    if movie == "" and len(categories) == 0:
        categories_liked_filtered = [
            category['name'] for category in categories_liked if category['rating'] >= 3]
        if len(categories_liked_filtered) == 0:
            categories_liked = [category['name'] for category in categories_liked]
            categories , relevance = get_relevance(categories_liked)
            movies = movie_recomm.recommend_given_categories(categories , relevance, top_k = 50)

        else :
            categories , relevance = get_relevance(categories_liked_filtered)
            movies = movie_recomm.recommend_given_categories(categories , relevance, top_k = 50)

    elif movie != "":
        movies = movie_recomm.general_recommendation(
            movie_recomm.get_movie_id(movie)[0])["similar_movies"]

    elif len(categories) != 0:
        categories , relevance = get_relevance(categories[:,0])
        movies = movie_recomm.recommend_given_categories(categories , relevance, top_k = 50)

    genres = list(movies["genres"])
    movies = list(movies["title"])
    user_movies = [movie['name'] for movie in user['movies']]
    movies_filtered = []
    genres_filtered = []
    for index, movie in enumerate(movies):
        if movie not in user_movies:
            movies_filtered.append(movie)
            genres_filtered.append(genres[index])
    movies_filtered = movies_filtered[:2]

    for index, movie in enumerate(movies_filtered):
        add_movie(user, movie,genres_filtered[index])
    text = send_recommendation(text, "movies", movies_filtered)
    response = {'text': text, 'movies': movies_filtered}
    return response


def get_relevance(categories):
    if len(categories) == 1:
        return categories, [0.8]
    if len(categories) == 2:
        return categories, [0.6, 0.6]
    return categories[:3], [0.5, 0.5, 0.5]


def locations_recommendation(user, preprocessed_text, text, location):
    print("calling the locations module...")
    location_tuple = (location['latitude'], location['longitude'])
    location_data = location_recomm.recommend(location_tuple ,keyword=preprocessed_text)
    locations = list()
    for loc in location_data[:2]:
        locations.append(
            {"الاسم": loc["name"], "تقييم المكان ": loc["rating"], "العنوان": loc["vicinity"]})
    for loc in locations:
        place = loc['الاسم']
        address = loc['العنوان']
        add_place(user, place, address)
    text = send_recommendation(text, "places", locations)
    response = {'text': text}
    return response


if __name__ == "__main__":
    print("loading models....")
    stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer, recomm_intent_model, recomm_tokenizer, location_recomm, movie_recomm,q_not_model , tf_idf_q_not = main.get_models()
    print("finished loading models")
    app.run(debug=True)
