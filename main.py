import math

from function import list_of_files, lowercase, copy, remove_punctuation, tf_a_file, list_of_import, list_of_export, idf, \
    tf_total

speeches_directory = "./speeches"
cleaned_directory = "./cleaned"

speechesNominationList = list_of_files(speeches_directory, "txt")
cleanedNominationList = list_of_files(cleaned_directory, "txt")

listNames = []
names = []

for i in range(len(speechesNominationList)):
    speeches_without_numbers = str(speechesNominationList[i][11:-4])
    listNames.append(speeches_without_numbers)

for i in listNames:

    if i[-1].isdigit():
        name = i[:-1]
    else:
        name = i

    names.append(name)

presidentNames = set(names)
presidentNames = list(presidentNames)

print("Voici les noms des présidents ayant fait des discours : ")

for i in range(len(presidentNames)):
    print(presidentNames[i], end=", ")
print("\n")

list_import = list_of_import(speechesNominationList)
list_export = list_of_export(cleanedNominationList)

for i in range(len(list_import)):
    copy(list_import[i], list_export[i])
    remove_punctuation(list_export[i])
    lowercase(list_export[i], list_export[i])

idf = idf(list_export)
print(idf)



total_tf = {}
for file in list_export:
    temp = tf_a_file(file)
    for term, frequency in dict.items(temp):
        total_tf[term] = frequency

print(total_tf)
