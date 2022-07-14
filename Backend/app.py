
from urllib import request
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import warnings
import sys
import os
import requests
from datetime import datetime
import numpy as np
warnings.filterwarnings("ignore")

module_path = os.path.abspath(os.path.join(
    'E:\Anees\Modules\Chatbot\src'))
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
    text = request.json['text']
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"

    intent, emotion, response = main.main(text, stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf,
                                          intent_model, tokenizer, recomm_intent_model, recomm_tokenizer, location_recomm, movie_recomm)
    print("Intent -> ", intent)
    print("Emotion ->", emotion)
    add_emotion(user, emotion)

    if intent == 'general' or intent == 'greeting' or intent == 'thank':
        messages = user['messages']
        if len(messages) > 4:
            messages = messages[:4]
        messages = messages[::-1]
        response = requests.post(
            'http://6259-34-147-54-199.ngrok.io/arz', json={'utter': text, 'history': messages})
        response = response.json()
        add_conversation(user, text, 1)
        add_conversation(user, response['response'], 0)

    elif intent == 'recommendation-movies':
        response = movies_recommendation(user, response['movie'], response['categories'], "")
        add_conversation(user, text, 1)
        add_conversation(user, response['text'], 0)

    elif intent == 'recommendation-places':
        response = locations_recommendation(user, response['places'], "")
        add_conversation(user, text, 1)
        add_conversation(user, response['text'], 0)

    return {'response': response, 'intent': intent}

# intents ->  recommendation-movies, recommendation-places, schedule, weather, general, *search*, None


@app.route('/history', methods=['POST'])
def get_history():
    username = request.json['username']
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    history = user['messages']
    return {'response': history, 'intent': 'history'}


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
                                'movies_categories_liked': movies_categories_liked, 'movies': [], 'places': [], 'emotions': ["joy"], 'messages': []})
    return "the user is created successfully"


@app.route('/emotions', methods=['GET'])
def get_most_frequent_emotion():
    username = request.json['username']
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    emotions = user['emotions']
    # get most frequent emotion using the last 5 messages
    if len(emotions) < 5:
        return {}, "None"
    most_frequent_emotion = max(set(emotions[:5]), key=emotions.count)
    response = {}
    intent = "None"
    if most_frequent_emotion == 'sadness':
        intent = "recommendation-movies-auto"
        response = movies_recommendation(user, "", np.array(
            [['comedy', 5], ['musical', 5]]), "من محادثاتك الاخيرة معايا حسيت انك حزين\n")

    elif most_frequent_emotion == 'anger':
        intent = "recommendation-places-auto"
        response = locations_recommendation(
            user, "عايز اروح مكان هادى", "من محادثاتك الاخيرة معايا حسيت انك متدايق\n")

    return {'response': response, 'intent': intent}


@app.route('/update_place_rating', methods=['PUT'])
def update_place_rating():
    username = request.json['username']
    place_name = request.json['place_name']
    rating = request.json['rating']
    rating = max(min(rating, 5), 0)
    user = usersCollection.find_one({'username': username})
    if user == None:
        return "there is no user with this username"
    places = user['places']
    for place in places:
        if place['name'] == place_name:
            place['rating'] = rating
            break
    usersCollection.update_one({'username': username}, {
        '$set': {'places': places}})
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
    usersCollection.update_one({'username': username}, {
                               '$set': {'movies': movies}})


def add_place(user, placeName, address, rating=2.5):
    username = user['username']
    places = user['places']
    place = {'name': placeName, 'rating': rating,
             'address': address, 'duration': 0}
    places.insert(0, place)
    usersCollection.update_one({'username': username}, {
                               '$set': {'places': places}})


def add_conversation(user, message, id):
    username = user['username']
    messages = user['messages']
    messageDB = {'isUser':id, 'message': message, 'time': datetime.now()}
    messages.insert(0, messageDB)
    usersCollection.update_one({'username': username}, {
                               '$set': {'messages': messages}})


def send_recommendation(text, type, contents):
    if type == "movies":
        text += "جبتلك فيلمين اهو ياريت يعجبوك\n\n"
        text += contents[0] + "\n\n"
        text += contents[1] + "\n\n"
        text += "\nوكمان شوية هبعتلك رسالة تقولى رأيك فيهم لو كونت شوفتهم"
    else:
        text += "جبتلك مكانين اهو ياريت يعجبوك\n\n"
        for content in contents:
            text += "الاسم : " + content['الاسم'] + "\n"
            text += "العنوان : " + content['العنوان'] + "\n\n"
        text += "\nوكمان شوية هبعتلك رسالة تقولى رأيك فيهم لو كونت زرتهم"
    return text


def movies_recommendation(user, movie, categories, text):
    print("calling the movies module...")
    categories_liked = user['movies_categories_liked']
    if movie == "" and len(categories) == 0:
        categories_liked_filtered = [
            category['name'] for category in categories_liked if category['rating'] >= 3]
        print(categories_liked_filtered)
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

    movies = list(movies["title"])
    user_movies = [movie['name'] for movie in user['movies']]
    movies_filtered = []
    print(user_movies)
    for movie in movies:
        if movie not in user_movies:
            movies_filtered.append(movie)
    print(movies_filtered)
    movies_filtered = movies_filtered[:2]

    for movie in movies_filtered:
        add_movie(user, movie)
    text = send_recommendation(text, "movies", movies_filtered)
    response = {'text': text}
    return response


def get_relevance(categories):
    if len(categories) == 1:
        return categories, [0.8]
    if len(categories) == 2:
        return categories, [0.6, 0.6]
    return categories[:3], [0.5, 0.5, 0.5]


def locations_recommendation(user, preprocessed_text, text):
    print("calling the locations module...")
    location_data = location_recomm.search_by_text(preprocessed_text)
    locations = list()
    for loc in location_data[:3]:
        locations.append(
            {"الاسم": loc["name"], "تقييم المكان ": loc["rating"], "العنوان": loc["formatted_address"]})
    for loc in locations:
        place = loc['الاسم']
        address = loc['العنوان']
        add_place(user, place, address)
    text = send_recommendation(text, "places", locations)
    response = {'text': text}
    return response


if __name__ == "__main__":
    print("loading models....")
    stopwords, ner_instance, verbs, nouns, emotions_model, emotions_tf_idf, intent_model, tokenizer,recomm_intent_model,recomm_tokenizer,location_recomm,movie_recomm = main.get_models()
    print("finished loading models")
    app.run(debug=True)
