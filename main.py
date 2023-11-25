import os
from function import list_of_files, minuscule

directory = "./speeches"
copy_folder = "./cleaned"

speechesNominationList = list_of_files(directory, "txt")
copy_truc = list_of_files(copy_folder, "txt")

list_names = []
names = []

for i in range(len(speechesNominationList)):
    speeches_without_numbers = str(speechesNominationList[i][11:-4])
    list_names.append(speeches_without_numbers)

for i in list_names:

    if i[-1].isdigit():
        name = i[:-1]
    else:
        name = i

    names.append(name)

president_names = set(names)
president_names = list(president_names)

print("Voici les noms des présidents ayant fait des discours : ")

for i in range(len(president_names)):

    print(president_names[i], end=", ")

for i in speechesNominationList:

    for y in copy_truc:

        minuscule(speechesNominationList[i], copy_truc[y])
