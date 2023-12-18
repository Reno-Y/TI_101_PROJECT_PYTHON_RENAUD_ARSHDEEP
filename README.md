# Projet ChatBot

Dans le cadre du projet du cours TI-101n voici une présentation du projet.

Création d'un chat bot dans l'optique d'une meilleure compréhension de chat-GPT
Ce programme permet d'analyser des textes afin dand un premier temps permettre de répondre à questions prédéfini et dans un autre temps répondre à des questions tel un chatbot classique.

Le programme permet donc :

-de prendre en compte un répertoire de fichier contenant des textes,
-les traités afin de pouvoir facilité la compréhension du texte par le programme,
-calculer un "term frequency - inverse document frequency" en fonction de ce qui lui est donné
-répondre à une question posé
Cependant la réponse à une question posé n'est pas très fonctionel du à une incompréhension lors du calcul du tf-df.

## Installation et éxecution : 

Afin de lancer le programe veuillez vous assurer que tout les ficihers sont dans un meme répertoire. De plus veuillez éxecuter le fichier "main.py"

```bash
git clone https://github.com/Reno-Y/TI_101_PROJECT_PYTHON_RENAUD_ARSHDEEP.git
```
Et enfin run le fichier:
-  [main.py](https://github.com/Reno-Y/TI_101_PROJECT_PYTHON_RENAUD_ARSHDEEP/blob/main/main.py)

## Guide d'utilisation :

* lors de l'éxécution du programme veuillez sélectionner si vous voulez accéder à la partie une du projet ou la partie chatbot
    1. Accéder aux fonctionnalités de la partie 1
        1. Afficher la liste des mots les moins importants
        2. Afficher le(s) mot(s) ayant le score TF-IDF le plus élevé
        3. Afficher le(s) mot(s) le(s) plus répété(s) par Chirac
        4. Afficher le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et le plus de fois
        5. Afficher le(s) premier(s) président(s) qui ont parlé de climat
        0. Quitter le menu des fonctionnalités

    2. Accéder au mode Chatbot
        1. Poser une question
        0. Quitter le menu Chatbot
    

## Bug

Il y a un bug lorsqu'on pose une question dans la section 2.1. Le programme ne renvoie pas la phrase pour la question souhaiter si une phrase est complexe voire meme pas tout dans certains cas.

Cepndant si vous signalez d'autres bug veuillez les reporter via :
[issues](https://github.com/Reno-Y/TI_101_PROJECT_PYTHON_RENAUD_ARSHDEEP/issues)

## [Contributeurs]
- [Renaud Yoganathan](https://github.com/Reno-Y)
- [Arshdeep Singh](https://github.com/Arshdeep931)
