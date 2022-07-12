from urllib import request
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import sys
import os
module_path = os.path.abspath(os.path.join('E:\GP\Anees\Anees\Modules\Chatbot\src'))
if module_path not in sys.path:
    sys.path.append(module_path)
import main

stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,location_recomm,movie_recomm = main.get_models()
# directory problem
# call the models to load before using them
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = "mongodb://localhost:27017/Anees"
mongo = PyMongo(app)
usersCollection = mongo.db.users


@app.route('/getResponse', methods=['GET'])
def get_response():
    username = request.json['username']
    text = request.json['text']
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    
    intent ,emotion ,response = main.main(text,stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,location_recomm,movie_recomm)
    add_emotion(user, emotion)
    if intent == 'recommendation-movies':
        movies = response["movies"]
        for movie in movies:
            add_movie(user, movie)
    elif intent == 'recommendation-places':
        locations = response["places"]
        for loc in locations:
            place = loc['الاسم']
            address = loc['العنوان']
            add_place(user, place, address)
    return {'response': response, 'intent': intent}
# intents ->  recommendation-movies, recommendation-places, schedule, weather, general, *search*, None


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = usersCollection.find_one(
        {'username': username, 'password': password})
    if user != None:
        return "logged in successfully"
    return "username or password in incorrect"


@app.route('/signup', methods=['POST'])
def sign_up():
    username = request.json['username']
    password = request.json['password']
    user = usersCollection.find_one({'username': username})
    if user != None:
        return "the username is already used"
    # add all the categories with 0 rating
    all_categories = ['action', 'adventure', 'animation', 'children', 'comedy', 'crime', 'documentary',
                      'drama', 'fantasy', 'horror', 'musical', 'mystery', 'romance', 'sci-fi', 'war', 'western']
    movies_categories_liked = []
    for category in all_categories:
        movies_categories_liked.append({'name': category, 'rating': 0})
    usersCollection.insert_one({'username': username, 'password': password,
                                'movies_categories_liked': movies_categories_liked, 'movies': [], 'places': [], 'emotions': ["joy"]})
    return "the user is created successfully"


@app.route('/emotions', methods=['get'])
def get_most_frequent_emotion():
    username = request.json['username']
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    emotions = user['emotions']
    # get most frequent emotion using half of his last messages
    most_frequent_emotion = max(set(emotions), key=emotions.count)
    response = {}
    intent = "None"
    if most_frequent_emotion == 'anger':
        intent = "recommendation-movies-auto"
        categories_liked = user['movies_categories_liked']
        # call the recommendation movies using the categories liked
        movie = "movie_recommended"
        add_movie(user, movie)
        response = {'movie': movie}
    elif most_frequent_emotion == 'sadness':
        intent = "recommendation-places-auto"
        place = ""
        longitude = ""
        latitude = ""
        add_place(user, place, longitude, latitude)
        # call the recommendation places using the most frequent place
        response = {'place', place}
    return {'response': response, 'intent': intent}


@app.route('/update_place_rating', methods=['PUT'])
def update_place_rating():
    username = request.json['username']
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    rating = request.json['rating']
    rating = max(min(rating, 5), 0)
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    range_of_longitude_search = 1
    places = user['places']
    flag = 0
    for place in places:
        if (place['longitude'] >= longitude - range_of_longitude_search and place['longitude'] <= longitude + range_of_longitude_search
                and place['latitude'] >= latitude - range_of_longitude_search and place['latitude'] <= latitude + range_of_longitude_search):
            place['rating'] = rating
            flag = 1
            break
    if flag:
        usersCollection.update_one({'username': username}, {
                                   '$set': {'places': places}})
    else:
        add_place(user, "new_place", longitude, latitude, rating)
    return "success"


@app.route('/update_movie_rating', methods=['PUT'])
def update_movie_rating():
    username = request.json['username']
    movie_name = request.json['movie_name']
    rating = request.json['rating']
    rating = max(min(rating, 5), 0)
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    movies = user['movies']
    flag = 0
    for movie in movies:
        if movie['name'] == movie_name:
            movie['rating'] = rating
            flag = 1
    if flag:
        usersCollection.update_one({'username': username}, {
                                   '$set': {'movies': movies}})
    else:
        add_movie(user, movie_name, rating)
    return "success"


@app.route('/update_category_rating', methods=['PUT'])
def update_category_rating():
    username = request.json['username']
    category_name = request.json['category_name']
    rating = request.json['rating']
    rating = max(min(rating, 5), 0)
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    movies_categories_liked = user['movies_categories_liked']
    for category in movies_categories_liked:
        if category['name'] == category_name:
            category['rating'] = rating
    usersCollection.update_one({'username': username}, {
                               '$set': {'movies_categories_liked': movies_categories_liked}})
    return "success"


def add_emotion(user, emotion):
    username = user['username']
    emotions = user['emotions']
    emotions.insert(0, emotion)
    usersCollection.update_one({'username': username}, {
                               '$set': {'emotions': emotions}})


def add_movie(user, movieName, rating=2.5):
    username = user['username']
    movies = user['movies']
    movie = {'name': movieName, 'rating': rating}
    movies.insert(0, movie)
    usersCollection.update_one({'username': username}, {'$set': {'movies': movies}})


def add_place(user, placeName, address, rating=2.5):
    username = user['username']
    places = user['places']
    place = {'name': placeName, 'rating': rating,
             'address': address, 'duration': 0}
    places.insert(0, place)
    usersCollection.update_one({'username': username}, {'$set': {'places': places}})


if __name__ == "__main__":
    app.run(debug=True)