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
**Anees** is an Arabic chatbot that can speak to users in different topics or an open-domain multi-turn conversation rather than a specific domain. Anees is your personal AI friend that you can express and witness yourself through a helpful and empathetic conversation.

## 📝 Table of Contents
- [Demo](#demo)
- [Architecture](#arch)
- [Datasets](#datasets)
- [Installation](#install)

## Demo <a name = "demo"></a>
<div align="center">

Demo 1 | Demo 2
:-: | :-:
<video src='https://user-images.githubusercontent.com/40968967/180667178-64b55cac-6661-43ad-8fd7-c3f8bf614758.mp4'/> | <video src='https://user-images.githubusercontent.com/40968967/180666812-15ede875-c0a6-4357-94e1-09885eadee7a.mp4'/>

</div>

## Architecture <a name = "arch"></a>

Anees consists of 6 major modules that need to be understood before starting implementing such a thing. The modules are natural language understanding, emotion classification, intent classification, weather/schedule, recommendation, and natural language generation. Apart from that, there is the connection between each module and the other. Each of these modules are described in detail in the project [documentation](https://github.com/aashrafh/Anees/blob/rest/Anees%20Document.pdf), how they all connected to each other, and how they represent the system architecture.

<div align="center">

![architecture](https://user-images.githubusercontent.com/40968967/180667782-8d183eb9-ca4d-4ff2-b774-8a6afa15f2b0.png)

</div>

## Datasets <a name = "datasets"></a>

We used different datasets for each module that suit the purpose of the module. Some of the used datasets are [ANERcorp](https://camel.abudhabi.nyu.edu/anercorp/), [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/), and [Arramooz](https://github.com/linuxscout/arramooz). You can download the used datasets from [Google Drive](https://drive.google.com/file/d/1tl2nmpfp6-V4WQmEhQSyrxGFGDm5wYbW/view?usp=sharing) and you can find the detasets used to fine-tune the GPT-2 model in the [this repository](https://github.com/aashrafh/anees-dataset).

## Installation <a name = "install"></a>
