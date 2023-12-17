from os import listdir, system, name
from math import log10
from collections import defaultdict


def list_of_files(directory, extension):
    files_names = []

    for filename in listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def list_of_import(speecherNominationList):
    """
    :param speecherNominationList: liste des fichiers dans le répertoire speeches
    :return: une liste des fichiers dans le répertoire speeches
    """
    temp_list = []
    for i in range(len(speecherNominationList)):
        file_path = "./speeches/" + str(speecherNominationList[i])
        temp_list.append(file_path)
    return temp_list


def list_of_export(cleanedNominationList):
    """
    :param cleanedNominationList: liste des fichiers dans le répertoire cleaned
    :return: une liste des fichiers dans le répertoire cleaned
    """
    temp_list = []
    for i in range(len(cleanedNominationList)):
        file_path = "./cleaned/" + str(cleanedNominationList[i])
        temp_list.append(file_path)
    return temp_list


LastNames_Names = {"Hollande": "François ",
                   "Chirac": "Jacques",
                   "Giscard_dEstaing": "Valéry",
                   "Macron": "Emmanuel",
                   "Mitterrand": "François",
                   "Sarkozy": "Nicolas"}


def extraction_of_presidents_names(speeches):
    """
    :param speeches: liste des fichiers dans le répertoire speeches
    :return: un dictionnaire associant président : list[fichier]
    """
    association = {}
    for speech in speeches:
        if speech[:11] == "Nomination_" and speech[-4:] == ".txt":
            name = speech[11:-4]
            if name[-1].isdigit():
                name = name[:-1]
            if name not in association:
                association[name] = []
            association[name].append(speech)

    return association


def association_of_names(speeches):
    """
    :param speeches: liste des fichiers dans le répertoire speeches
    :return: un dictionnaire avec les noms des présidents et leurs prénoms
    """
    Name_LastNames = {}
    for name in extraction_of_presidents_names(speeches):
        Name_LastNames[name] = LastNames_Names[name]
    Name_LastNames = dict(map(reversed, Name_LastNames.items()))

    return Name_LastNames


def open_file(path):
    with open(path, "r", encoding='utf-8') as file:
        return file.read()


def write_to_file(path, text):
    with open(path, "w", encoding='utf-8') as file:
        file.write(text)


def copy(old_file, new_file):
    text = open_file(old_file)
    write_to_file(new_file, text)


def remove_punctuation(file):
    """

    :param file: le fichier à nettoyer
    :return: un fichier sans ponctuation
    """
    text = open_file(file)
    characters_to_remove = {'"': ' ', ',': ' ', '-': ' ', '.': ' ', "'": ' ', '!': ' ', ':': ' ', ';': ' ', '`': ' ',
                            '?': ' '}
    cleaned_text = ''.join(characters_to_remove.get(char, char) for char in text)
    write_to_file(file, cleaned_text)


def toLowercase(file, destination_file):
    """

    :param file: le fichier à rendre en minuscule
    :param destination_file: le fichier de destination avec les minuscules
    :return:
    """
    text = open_file(file)
    output = text.lower()
    write_to_file(destination_file, output)


def clean_all_files(list_import, list_export):
    for i in range(len(list_import)):
        copy(list_import[i], list_export[i])
        remove_punctuation(list_export[i])
        toLowercase(list_export[i], list_export[i])


def termsFrequency(words):
    """
    Principe du tf
    :param words: mots à analyser
    :return: un dictionnaire avec le compte des mots
    """
    word_count = {}

    for word in words:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1

    return word_count


def termsFrequencyOfFile(file):
    """
    :param file: le fichier à analyser
    :return: Renvoie le tf d'un fichier
    """
    mots = open_file(file).split()
    return termsFrequency(mots)


def TermFrequencyOfAText(text):
    """
    :param text: le texte à analyser
    :return: Renvoie le tf d'un texte
    """
    mots = text.split()
    return termsFrequency(mots)


def tf_total(list_export):
    """
    :param list_export: liste des fichiers à tf
    :return: Renvoi le tf total de tous les fichiers
    """
    tf_score = {}
    for file in list_export:
        tf = termsFrequencyOfFile(file)

        for term, frequency in tf.items():
            if term not in tf_score:
                tf_score[term] = frequency
            else:
                tf_score[term] += frequency
    return tf_score


def idf(list_export):
    """
    :param list_export: liste des fichiers des à traiter
    :return: le score idf de tous les mots dans les textes d'un répertoire
    """
    idf_score = {}
    tf_score = tf_total(list_export)
    nb_documents = len(list_export)

    for i in tf_score:
        idf_score[i] = round(log10((nb_documents / tf_score[i]) + 1), 2)
    return idf_score


def idf_specific_list(list_of_file, tf_score):
    """
    Permet d'idf une liste spécifique de fichiers
    :param list_of_file:
    :param tf_score:
    :return:
    """
    nb_documents = len(list_of_file)
    for i in tf_score:
        tf_score[i] = round(log10((nb_documents / tf_score[i]) + 1), 2)
    return tf_score


def tf_idf(list_export):
    """
    :param list_export: list des fichiers dans le répertoire cleaned
    :return: une matrice tf idf avec les mots en ligne et les fichiers en colonne
    """

    idf_global = idf(list_export)
    tf_idf = {}

    all_files = {}
    for file in list_export:
        all_files[file] = termsFrequencyOfFile(file)
    for word in idf_global:
        tf_idf[word] = {}  # On crée une nouvelle ligne dans la matrice
        for file in all_files:
            tf = all_files[file]  # On récupère le tf du fichier
            if word in tf:
                tf_idf[word][file] = tf[word] * idf_global[word]
            else:
                tf_idf[word][file] = 0  # Si le mot n'est pas dans le fichier on rajoute un 0 à sa valeur
    return tf_idf


def tf_idf_matrix(list_export):
    """
    :param list_export:
    :return: Création d'une matrice tf idf avec les mots en ligne et les fichiers en colonne
    """
    tf_idf_with_file = tf_idf(list_export)
    final_matrix = {}

    for word, score in tf_idf_with_file.items():
        values_for_word = list(score.values())
        final_matrix[word] = values_for_word

    return final_matrix


def less_important_words(list_export):
    """
    créer une liste des mots les idf les moins importants
    :param list_export: liste des fichiers dans le répertoire cleaned
    :return: une liste des mots les moins importants
    """

    matrix = tf_idf(list_export)

    less_important_words_list = []
    for word in matrix:
        score_sum = 0
        for text in matrix[word]:
            score_sum += matrix[word][text]
        score = score_sum / len(list_export)
        if score <= 0:
            less_important_words_list.append(word)

    return less_important_words_list


def max_tfidf_words(list_export):
    """
    :param list_export: liste des fichiers dans le répertoire cleaned
    :return: le(s) mot(s) avec le score tf-idf le plus élevé
    """
    matrix = tf_idf(list_export)
    score_max = 0
    list_words = []

    for word in matrix:
        for text in matrix[word]:
            score = matrix[word][text]
            if score > score_max:  # Si le nouveau score est plus élevé alors, on change le mot
                score_max = score
                list_words = [word]
            elif score == score_max:  # Si le nouveau score est égal alors, on rajoute le mot
                list_words.append(word)

    return list_words


def MostRepeatedWords(speeches, president_name):
    """
    :param speeches: Liste des dicours du président dans le répertoir
    :param president_name: Liste des noms, prénoms des présidents
    :return:
    """

    president_speeches = extraction_of_presidents_names(speeches)[president_name]

    for file in president_speeches:
        location = "./cleaned/" + file
        all_text = open_file(location)

    tf = TermFrequencyOfAText(all_text)
    exempted_words = ["le", "la", "les", "de", "du", "des", "et", "en", "à", "dans", "un", "une", "au", "aux", "par",
                      "l", "d", "pour", "elle", "il", "ils", "elles", "ce", "cet", "cette", "ces", "qui", "que", "quoi",
                      "où", "quand", "comment", "pourquoi", "est", "sont", "ont", "a", "doit", "je", "n", "y", "s", "t",
                      "m", "me", "ma", "mes", "mon", "parce", "que", "veut", "j", "messieurs", "mesdames", "monsieur",
                      "madame", "mesdemoiselles", "pas", "nous"]
    # Liste des mots à ne pas prendre en compte

    max_occurrence = 0
    most_repeated_words = []
    new_words_tf = tf.copy()

    for word in tf:
        if word in exempted_words:
            new_words_tf.pop(word)  # On enlève les mots à ne pas prendre en compte

    for word in new_words_tf:
        if new_words_tf[word] > max_occurrence:
            max_occurrence = new_words_tf[word]
            most_repeated_words = [word]

    return most_repeated_words


def search_word(word, most):
    """
    :param word: le mot à rechercher
    :param most: booléen qui permet l'affichage ou non du président qui en parle le plus
    :return: le nom du (des) président(s) qui ont parlé d'un certain mot
    """
    matrix = tf_idf(list_of_export(list_of_files("./cleaned/", "txt")))
    list_of_presidents = association_of_names(list_of_files("./speeches/", "txt"))

    presidents_who_speak_about_word = []
    tfidf_max = 0
    president_max = ""

    for file in matrix[word]:
        if matrix[word][file] > 0:
            for president in list_of_presidents:
                if list_of_presidents[president] in file:
                    presidents_who_speak_about_word.append(list_of_presidents[president])
                if matrix[word][file] > tfidf_max:
                    tfidf_max = matrix[word][file]
                    president_max = list_of_presidents[president]

    print("Le(s) président(s) qui ont parlé de", '"', word, '"', "sont :", "\n")
    president_who_spoked_about = list(set(presidents_who_speak_about_word))
    for i in range(len(president_who_spoked_about)):
        print("-", president_who_spoked_about[i])
    print("\n")

    if most == True :
        print("Le président qui a le plus parlé de", '"', word, '"', "est :", president_max)


def menu():
    print("1. Afficher la liste des mots les moins importants")
    print("2. Afficher le(s) mot(s) ayant le score TF-IDF le plus élevé")
    print("3. Afficher le(s) mot(s) le(s) plus répété(s) par Chirac")
    print("4. Afficher le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et le plus de fois")
    print("5. Afficher le(s) premier(s) président(s) qui ont parlé de climat")
    print("0. Quitter le programme")
    print()


def menu_choice():
    choice = int(input("Veuillez choisir une option : "))
    while choice < 0 or choice > 6:
        print("Veuillez choisir un nombre entre 1 et 6")
        choice = int(input("Quel est votre choix ? "))
    if choice == 1:
        print("Les mots les moins importants sont :",
              less_important_words(list_of_export(list_of_files("./cleaned/", "txt"))))
    elif choice == 2:
        print("Le(s) mot(s) ayant le score TF-IDF le plus élevé est :",
              max_tfidf_words(list_of_export(list_of_files("./cleaned/", "txt"))))
    elif choice == 3:
        print("Le(s) mot(s) le(s) plus répété(s) par Chirac est :",
              MostRepeatedWords(list_of_files("./speeches/", "txt"), "Chirac"))
    elif choice == 4:
        print(search_word("nation", True))
    elif choice == 5:
        print(search_word("climat", False))
    elif choice == 0:
        exit()



if __name__ == "__main__":
    print("Please run the main file instead.")
