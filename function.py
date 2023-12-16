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
    temp_list = []
    for i in range(len(speecherNominationList)):
        file_path = "./speeches/" + str(speecherNominationList[i])
        temp_list.append(file_path)
    return temp_list


def list_of_export(cleanedNominationList):
    temp_list = []
    for i in range(len(cleanedNominationList)):
        file_path = "./cleaned/" + str(cleanedNominationList[i])
        temp_list.append(file_path)
    return temp_list


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
    text = open_file(file)
    characters_to_remove = {'"': ' ', ',': ' ', '-': ' ', '.': ' ', "'": ' ', '!': ' ', ':': ' ', ';': ' ', '`': ' ',
                            '?': ' '}
    cleaned_text = ''.join(characters_to_remove.get(char, char) for char in text)
    write_to_file(file, cleaned_text)


def lowercase(file, destination_file):
    text = open_file(file)
    output = text.lower()
    write_to_file(destination_file, output)


def tf(words):
    word_count = {}

    for word in words:
        if word not in word_count:
            word_count[word] = 1

    return word_count


def tf_a_file(file):
    mots = open_file(file).split()
    return tf(mots)


def tf_total(list_export):
    tf_score = {}
    for file in list_export:
        tf = tf_a_file(file)

        for term, frequency in tf.items():
            if term not in tf_score:
                tf_score[term] = frequency
            else:
                tf_score[term] += frequency
    return (tf_score)


def idf(list_export):
    tf_score = tf_total(list_export)
    nb_documents = len(list_export)

    for i in tf_score:
        tf_score[i] = round(math.log10((nb_documents / tf_score[i]) + 1), 2)
    return tf_score


def tf_idf_matrix(list_export):
    idf_global = idf(list_export)
    tf_idf = {}

    all_files = {}
    for file in list_export:
        all_files[file] = tf_a_file(file)

    for word in idf_global:
        tf_idf[word] = {}  # On crée une nouvelle ligne dans la matrice
        for file in all_files:
            tf = all_files[file]  # On récupère le tf du fichier
            if word in tf:
                tf_idf[word][file] = tf[word] * idf_global[word]
            else:
                tf_idf[word][file] = 0  # Si le mot n'est pas dans le fichier on rajoute un 0 à sa valeur
    return tf_idf


def less_important_words(list_export):

    matrix = tf_idf_matrix(list_export)

    less_important_words_list = []
    for word in matrix:
        score_sum = 0
        for text in matrix[word]:
            score_sum += matrix[word][text]
        score = score_sum / len(list_export)
        if score <= 0:
            less_important_words_list.append(word)

    return less_important_words_list
