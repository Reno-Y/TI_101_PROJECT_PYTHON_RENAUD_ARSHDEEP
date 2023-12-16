import math

from function import (
    association_of_names,
    list_of_files,
    toLowercase,
    copy,
    remove_punctuation,
    list_of_import,
    list_of_export,
    MostRepeatedWords,
    tf_idf_matrix)

SPEECHES_DIRECTORY_LIST = "./speeches/"
CLEANED_DIRECTORY = "./cleaned/"

speechesNominationList = list_of_files(SPEECHES_DIRECTORY_LIST, "txt")
cleanedNominationList = list_of_files(CLEANED_DIRECTORY, "txt")

list_import = list_of_import(speechesNominationList)
list_export = list_of_export(cleanedNominationList)

for i in range(len(list_import)):
    copy(list_import[i], list_export[i])
    remove_punctuation(list_export[i])
    toLowercase(list_export[i], list_export[i])


for word, values in tf_idf_matrix(list_export).items():
    print(f"{word} :{values}")



PRESIDENT_TO_SEARCH = str(input("Of which president you want to know is most repeated word ? "))

while PRESIDENT_TO_SEARCH not in association_of_names(cleanedNominationList).values():
    print(PRESIDENT_TO_SEARCH, " is not in the list of presidents")
    PRESIDENT_TO_SEARCH = str(input("Of which president you want to know is most repeated word ? "))

print(MostRepeatedWords(speechesNominationList, PRESIDENT_TO_SEARCH))

print(less_important_words(list_export))