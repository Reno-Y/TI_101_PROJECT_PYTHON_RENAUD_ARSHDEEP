import os
import math
from collections import defaultdict


def list_of_files(directory, extension):
    files_names = []

    for filename in os.listdir(directory):
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


LastNames_Names = {"Hollande": "François", "Chirac": "Jacques", "Giscard_dEstaing": "Valéry", "Macron": "Emmanuel",
                   "Mitterrand": "François", "Sarkozy": "Nicolas"}


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
    :return: une asso
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
    :return:
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
        idf_score[i] = round(math.log10((nb_documents / tf_score[i]) + 1), 2)
    return idf_score


def idf_specific_list(list_of_file, tf_score):
    nb_documents = len(list_of_file)
    for i in tf_score:
        tf_score[i] = round(math.log10((nb_documents / tf_score[i]) + 1), 2)
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
    tf_idf_with_file = tf_idf(list_export)
    final_matrix = {}

    for word, score in tf_idf_with_file.items():
        values_for_word = list(score.values())
        final_matrix[word] = values_for_word

    return final_matrix


def less_important_words(list_export):
    """
    créer une liste des mots les moins importants
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


def MostRepeatedWords(speeches, president_name):
    president_speeches = extraction_of_presidents_names(speeches)[president_name]

    for file in president_speeches:
        location = "./cleaned/" + file
        all_text = open_file(location)

    tf = TermFrequencyOfAText(all_text)

    return tf