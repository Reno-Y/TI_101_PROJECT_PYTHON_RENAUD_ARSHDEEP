# TI-101 PROJECT-PYTHON

Création d'un chat bot dans l'optique d'une meilleure compréhension de chat-GPT

Ce programme permet d'analyser des textes donner dans un répertoire afin de pouvoir donner un TF-IDF

Cependant le programme est incomplet du  à de nombreuses difficultées

la suppression de la ponctuation
-la conversion en minuscules
-le calcul du score tfn le score idf et le score tf-idf.

Il faut veiller à avoir tous les fichiers dans le même dossier. 

—————————————————————

Fonctions : 
 
list_of_files : permet de récupérer les noms de fichiers dans une liste 

list_of_import : permet de faire une liste avec le chemin qui donne accès à chaque fichier et rajouter « speecherNominationList[i] »
remove_punctuation : permet d'enlever la ponctuation et remplacer par un espace
lowercase : permet de convertir tout le texte en minuscules 
tf : permet de calculer le score tf
tf_idf : permet de calculer le score tdf-idf
