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
        if word in word_count:
            word_count[word] += 1
        else:
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
        tf_score[i] = math.log10((nb_documents / tf_score[i]) + 1)
    return tf_score


def tf_idf(list_directory):
    files = list_directory

    tf_score = tf_total(files)
    idf_score = idf(files)

    unique_words = list(set(tf_score.keys()))

    tfidf = []

    for word in unique_words:
        tfidf_line = []
        for file in files:
            tf = tf_a_file(file)
            tf_value = tf.get(word, 0)
            idf_value = idf_score.get(word, 0)
            tfidf_value = tf_value * idf_value
            tfidf_line.append(tfidf_value)
        tfidf.append(tfidf_line)

    return tfidf

