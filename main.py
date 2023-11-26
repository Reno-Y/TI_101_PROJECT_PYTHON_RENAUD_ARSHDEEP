from function import list_of_files, lowercase, copy, remove_punctuation, tf_a_file

directory = "./speeches"
copy_folder = "./cleaned"

speechesNominationList = list_of_files(directory, "txt")
cleanedNominationList = list_of_files(copy_folder, "txt")

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
print("\n")

list_import = []
for i in range(len(speechesNominationList)):
    cara = "./speeches/" + str(speechesNominationList[i])
    list_import.append(cara)

list_export = []
for i in range(len(cleanedNominationList)):
    cara = "./cleaned/" + str(cleanedNominationList[i])
    list_export.append(cara)

for i in range(len(list_import)):
    copy(list_import[i], list_export[i])
    remove_punctuation(list_export[i])
    lowercase(list_export[i], list_export[i])

print(tf_a_file("./cleaned/Nomination_Sarkozy_cleaned.txt"))

