import os

# on importe les fichiers

def list_of_files(directory, extension):

    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

directory = "./speeches"
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

president_names = set(names)
president_names = list(president_names)

print(president_names)
