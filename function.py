import os


def list_of_files(directory, extension):
    files_names = []

    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


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
    characters_to_remove = {'"': ' ', ',': ' ', '-': ' ', '.': ' ', "'": ' ', '!': ' ', ':': ' ', ';': ' '}
    cleaned_text = ''.join(characters_to_remove.get(char, char) for char in text)
    write_to_file(file, cleaned_text)


def lowercase(file, destination_file):
    text = open_file(file)
    output = text.lower()
    write_to_file(destination_file, output)


def tf(chaine):
    word_count = {}
    count = 1
    for mot in chaine:
        if mot not in word_count:
            word_count.update({mot: count})
        elif mot in word_count:
            word_count[mot] += 1
    return word_count


def tf_a_file(file):
    text = open_file(file).split(' ')
    return tf(text)
