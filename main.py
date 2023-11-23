import os
from function import *

# on importe les fichiers
directory = "./speeches"
copy_folder = "/cleaned"

speeches_names = list_of_files(directory, "txt")

list_names = []
names = []

for i in range(len(speeches_names)):
    nom = str(speeches_names[i][11:-4])   # on slice la liste pour n'avoir que le nom du président et le numéro
    list_names.append(nom)

# On a encore des chiffres, il faut donc les supprimer
for i in list_names:
    if i[-1].isdigit():
        name = i[:-1]
    # Si le dernier caractère est un chiffre alors on va slice la liste de façon à reculer d'un pas
    else:
        name = i
    # S'il n'y a pas de chiffre alors on ne fait rien
    names.append(name)

#on supprime les doublons
president_names = set(names)             
president_names = list(president_names)

print("Voici les noms des présidents ayant fait un discour : ")
for i in range(len(president_names)):
    print(president_names[i], end=", ")
#on copie les discours dans des autres fichiers afin de les traiter


cleaning_chirac1()