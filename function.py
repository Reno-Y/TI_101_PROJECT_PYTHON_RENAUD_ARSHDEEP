import os


def list_of_files(directory, extension):
    files_names = []

    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)

    return files_names


def open_file(path):
    with open(path, "r") as file:
        return file.read()


def write_to_file(path, text):
    with open(path, "w") as file:
        file.write(text)


def copy(old_file, new_file):
    text = open_file(old_file)
    write_to_file(new_file, text)


def clean(file):
    text = open_file(file)
    characters_to_remove = {'"': ' ', ',': ' ', '-': ' ', '.': ' ', "'": ' ', '!': ' '}
    cleaned_text = ''.join(characters_to_remove.get(char, char) for char in text)
    write_to_file(file, cleaned_text)


def remove_accent(file):
    text = open_file(file)
    accent = {'é': 'e', 'è': 'e', 'ê': 'e', 'à': 'a', 'ù': 'u', 'û': 'u', 'ç': 'c', 'ô': 'o', 'î': 'i', 'ï': 'i',
              'â': 'a'}
    text_without_accent = ''.join(accent.get(char) for char in text)
    write_to_file(file, text_without_accent)


def lowercase(file):
    text = open_file(file)
    write_to_file(file, text.lower())
