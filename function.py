import os


def list_of_files(directory, extension):
    files_names = []

    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)

    return files_names


def minuscule(fichier_ancien, fichier_nouveau):
    text = open_file(fichier_ancien)
    write_to_file(fichier_nouveau, text.strip(",."))


def open_file(path):
    with open(path, "r") as file:
        return file.read()


def write_to_file(path, text):
    with open(path, "w") as file:
        file.write(text)
