import math

from function import (
    association_of_names,
    list_of_files,
    toLowercase,
    copy,
    remove_punctuation,
    list_of_import,
    list_of_export,
    idf,
    tf_total,
    most_repeated_words)

SPEECHES_DIRECTORY_LIST = "./speeches/"
CLEANED_DIRECTORY = "./cleaned/"

speechesNominationList = list_of_files(SPEECHES_DIRECTORY_LIST, "txt")
cleanedNominationList = list_of_files(CLEANED_DIRECTORY, "txt")

print("Voici les noms des présidents ayant fait des discours : ")
for Name, LastName in association_of_names(speechesNominationList).items():
    print(Name, LastName)

list_import = list_of_import(speechesNominationList)
list_export = list_of_export(cleanedNominationList)

for i in range(len(list_import)):
    copy(list_import[i], list_export[i])
    remove_punctuation(list_export[i])
    toLowercase(list_export[i], list_export[i])

tf_score = tf_total(list_export)
idf_score = idf(list_export)

print(most_repeated_words(cleanedNominationList, "Chirac"))