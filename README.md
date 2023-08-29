<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=210px src="https://user-images.githubusercontent.com/40968967/180668398-0b453d43-a08f-4b31-ba22-6dcb71a3cb12.svg" alt="Anees logo"></a>
</p>

<p align="center"> :robot: Your personal AI friend.
    <br> 
</p>

<p align="center">
  <a href="https://github.com/aashrafh/Anees/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/aashrafh/Anees" /></a>
  
   <a href="https://github.com/aashrafh/Anees/issues" alt="Issues">
        <img src="https://img.shields.io/github/issues/aashrafh/Anees" /></a>
  
  <a href="https://github.com/aashrafh/Anees/network" alt="Forks">
        <img src="https://img.shields.io/github/forks/aashrafh/Anees" /></a>
        
  <a href="https://github.com/aashrafh/Anees/stargazers" alt="Stars">
        <img src="https://img.shields.io/github/stars/aashrafh/Anees" /></a>
        
  <a href="https://github.com/aashrafh/Anees/blob/master/LICENSE" alt="License">
        <img src="https://img.shields.io/github/license/aashrafh/Anees" /></a>
</p>


---

# Anees
**Anees** is an Arabic chatbot that can speak to users on different topics or an open-domain multi-turn conversation rather than a specific domain. Anees is your personal AI friend that you can express and witness yourself through a helpful and empathetic conversation.

## 📝 Table of Contents
- [Demo](#demo)
- [Architecture](#arch)
- [Datasets](#datasets)
- [Installation](#install)
- [Technology](#tech)

## Demo <a name = "demo"></a>
<div align="center">

Demo 1 | Demo 2
:-: | :-:
<video src='https://user-images.githubusercontent.com/40968967/180667178-64b55cac-6661-43ad-8fd7-c3f8bf614758.mp4'/> | <video src='https://user-images.githubusercontent.com/40968967/180666812-15ede875-c0a6-4357-94e1-09885eadee7a.mp4'/>

</div>

## Architecture <a name = "arch"></a>

Anees consists of 6 major modules that need to be understood before implementing such a thing. The modules are natural language understanding, emotion classification, intent classification, weather/schedule, recommendation, and natural language generation. Apart from that, there is a connection between each module and the other. Each of these modules is described in detail in the project [documentation](https://github.com/aashrafh/Anees/blob/rest/Anees%20Document.pdf), how they are all connected to each other, and how they represent the system architecture.

<div align="center">

![architecture](https://user-images.githubusercontent.com/40968967/180667782-8d183eb9-ca4d-4ff2-b774-8a6afa15f2b0.png)

</div>

## Datasets <a name = "datasets"></a>

We used different datasets for each module that suit the purpose of the module. Some of the used datasets are [ANERcorp](https://camel.abudhabi.nyu.edu/anercorp/), [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/), and [Arramooz](https://github.com/linuxscout/arramooz). You can find the datasets used to fine-tune the GPT-2 model in [this repository](https://github.com/aashrafh/anees-dataset).

## Installation <a name = "install"></a>

To install and run the project:

- For the modules, you need to install [Docker](https://docs.docker.com/engine/install/), [Docker Compose](https://docs.docker.com/compose/install/), and 
    1. Build the image:
    
    ```py 
    docker-compose build
    ```
    
    2. Run the image:
    
    ```py 
    docker-compose run
    ```
- For the client, you need to install [Node.js](https://nodejs.org/en/download/), [Expo](https://docs.expo.dev/get-started/installation/), and then:
    1. Install the dependencies:
    ```py
    npm install
    ```
    
    2. Run the client:
    ```py
    npm start
    ```
    
    3. Choose between running the client through an emulator or directly on your phone. Also, you can build an APK version for Android using:
    ```py
    expo build:android -t apk
    ```
    or for iOS:
    ```py
    expo build:ios -t archive
    ```
 - Alos, we provided interactive notebooks for each module that you can use to train, visualize, or have an idea of the implementation details.
 
 > Remember to update [`config.py`](https://github.com/aashrafh/Anees/blob/main/modules/config.py) with your [OpenWeatherMap](https://openweathermap.org/) API keys.
 
 ## ⛏️ Built Using <a name = "tech"></a>
- [Python](https://www.python.org/)
- [PyTorch](https://pytorch.org/)
- [scikit-learn](https://scikit-learn.org/stable/)
- [MongoDB](https://www.mongodb.com/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [React Native](https://reactnative.dev/)
- [Expo](https://expo.dev/)

## Collaboraters

<table>
  <tr>
    <td align="center"><a href="https://github.com/aashrafh"><img src="https://avatars.githubusercontent.com/u/40968967?v=4" width="150px;" alt=""/><br /><sub><b>Ahmed Ashraf</b></sub></a><br /></td>
     <td align="center"><a href="https://github.com/ahmedsherif304"><img src="https://avatars.githubusercontent.com/u/40776441?v=4" width="150px;" alt=""/><br /><sub><b>Ahmed Sherif</b></sub></a><br /></td>
     <td align="center"><a href="https://github.com/AhmedMGZ7"><img src="https://avatars.githubusercontent.com/u/48853566?v=4" width="150px;" alt=""/><br /><sub><b>Ahmed Magdy</b></sub></a><br /></td>
     <td align="center"><a href="https://github.com/Abdelrhmanfdl"><img src="https://avatars.githubusercontent.com/u/44409979?v=4" width="150px;" alt=""/><br /><sub><b>Abdelrhman Fdl</b></sub></a><br /></td>
  </tr>
 </table
  >
  
## Acknowledgment

This is our graduation project for a Bachelor of Science degree in Computer Engineering from Cairo University, in 2022.
