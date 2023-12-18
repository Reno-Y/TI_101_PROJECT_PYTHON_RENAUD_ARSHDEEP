from os import listdir, system, name
from math import log10, sqrt
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
    :return: une liste avec le chemin d'accès de chaque fichier dans le répertoire speeches
    """
    temp_list = []
    for i in range(len(speecherNominationList)):
        file_path = "./speeches/" + str(speecherNominationList[i])
        temp_list.append(file_path)
    return temp_list


def list_of_export(cleanedNominationList):
    """
    :param cleanedNominationList: liste des fichiers dans le répertoire cleaned
    :return: une liste avec le chemin d'accès de chaque fichier dans le répertoire cleaned
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
        if speech[:11] == "Nomination_" and speech[-4:] == ".txt":  # slice les noms des fichiers
            last_name = speech[11:-4]
            if last_name[-1].isdigit():  # vérifie si le dernier caractère est un chiffre
                last_name = last_name[:-1]
            if last_name not in association:
                association[last_name] = []
            association[last_name].append(speech)

    return association


def association_of_names(speeches):
    """
    :param speeches: liste des fichiers dans le répertoire speeches
    :return: un dictionnaire avec les noms des présidents et leurs prénoms
    """
    name_last_names = {}
    for name in extraction_of_presidents_names(speeches):
        name_last_names[name] = LastNames_Names[name]
    name_last_names = dict(map(reversed, name_last_names.items()))  # Inverse les clés et les valeurs

    return name_last_names


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
                            '?': ' '}  # Dictionnaire des caractères à supprimer
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
    """
    Nettoie tous les fichiers d'un répertoire
    :param list_import: list des fichiers à nettoyer
    :param list_export: list des fichiers nettoyés
    :return:
    """
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
    for word, val in word_count.items():
        word_count[word] /= len(words)

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


def TermFrequencyTotal(list_export):
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


def InverseDocumentFrequency(list_export):
    """
    :param list_export: liste des fichiers à traiter
    :return: le score idf de tous les mots dans des textes d'un répertoire
    """
    idf_score = {}
    tf_score = TermFrequencyTotal(list_export)
    nb_documents = len(list_export)

    for i in tf_score:
        idf_score[i] = round(log10((nb_documents / tf_score[i]) + 1), 2)
    return idf_score


def InverseDocumentFrequencyAList(list_of_file, tf_score):
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


def TFIDF(list_export):
    """
    :param list_export: list des fichiers dans le répertoire cleaned
    :return: une matrice tf idf avec les mots en ligne et les fichiers en colonne
    """

    idf_global = InverseDocumentFrequency(list_export)
    tf_idf = {}

    all_files = {}
    for file in list_export:
        all_files[file] = termsFrequencyOfFile(file)
    for word in idf_global:
        tf_idf[word] = {}  # On crée une nouvelle ligne dans la matrice
        for file in all_files:
            tf = all_files[file]  # On récupère le tf du fichier
            if word in tf:
                tf_idf[word][file] = round((tf[word] * idf_global[word]), 2)
            else:
                tf_idf[word][file] = 0  # Si le mot n'est pas dans le fichier on rajoute un 0 à sa valeur
    return tf_idf


def TFIDFMatrix(list_export):
    """
    :param list_export:
    :return: Création d'une matrice tf idf avec les mots en ligne et les fichiers en colonne
    """
    tf_idf_with_file = TFIDF(list_export)
    final_matrix = {}

    for word, score in tf_idf_with_file.items():
        values_for_word = list(score.values())
        final_matrix[word] = values_for_word

    return final_matrix


def LessImportantWords(list_export):
    """
    Créer une liste des mots les moins importants
    :param list_export: liste des fichiers dans le répertoire cleaned
    :return: une liste des mots les moins importants
    """

    matrix = TFIDF(list_export)

    less_important_words_list = []
    for word in matrix:
        score_sum = 0
        for text in matrix[word]:
            score_sum += matrix[word][text]
        score = score_sum / len(list_export)
        if score <= 0:
            less_important_words_list.append(word)

    return less_important_words_list


def MaxTFIDFWords(list_export):
    """
    :param list_export: liste des fichiers dans le répertoire cleaned
    :return: le(s) mot(s) avec le score tf idf le plus élevé
    """
    matrix = TFIDF(list_export)
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
        all_text = open_file(location)  # On crée un fichier avec tous les discours du président

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


def SearchWord(word, most):
    """
    :param word: le mot à rechercher
    :param most: booléen qui permet l'affichage ou non du président qui en parle le plus
    :return: le nom du (des) président(s) qui ont parlé d'un certain mot
    """
    matrix = TFIDF(list_of_export(list_of_files("./cleaned/", "txt")))
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

    if most:
        print("Le président qui a le plus parlé de", '"', word, '"', "est :", president_max)


def MainMenu():
    print("1. Accéder aux fonctionnalités de la partie 1")
    print("2. Accéder au mode Chatbot")
    print("0. Quitter le programme")
    print()
    main_menu_choice()


def main_menu_choice():
    print()
    choice = int(input("Veuillez choisir une option : "))
    while choice < 0 or choice > 2:
        print("Veuillez choisir un nombre entre 0 et 2")
        choice = int(input("Quel est votre choix ? "))
    if choice == 0:
        exit()
    if choice == 1:
        Menu()
    if choice == 2:
        MenuChatBot()

def MenuChatBot():
    print()
    print("1. Poser une question")
    print("0. Quitter le menu Chatbot")
    print()
    MenuChatBotChoice()

def MenuChatBotChoice():
    choice = int(input("Veuillez choisir une option : "))
    while choice < 0 or choice > 1:
        print("Veuillez choisir un nombre entre 0 et 1")
        choice = int(input("Veuillez choisir une option ? "))

    if choice == 0:
        MainMenu()
    elif choice == 1:
        question = str(input("Posez votre question : "))
        list_export = list_of_export(list_of_files("./cleaned/", "txt"))
        dict_tf_question = TFOfAQuestion(question, list_export)
        idf_total = InverseDocumentFrequency(list_export)

        question_token = TokenizeQuestion(question)

        vector_question = TFIDFVectorQuestion(dict_tf_question, idf_total, question)

        print((ResponseOfQuestion(question_token)),
              SentenceOfQuestion(vector_question, dict_tf_question, idf_total, question))


def Menu():
    print()
    print("1. Afficher la liste des mots les moins importants")
    print("2. Afficher le(s) mot(s) ayant le score TF-IDF le plus élevé")
    print("3. Afficher le(s) mot(s) le(s) plus répété(s) par Chirac")
    print("4. Afficher le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et le plus de fois")
    print("5. Afficher le(s) premier(s) président(s) qui ont parlé de climat")
    print("0. Quitter le menu des fonctionnalités")
    print()
    MenuChoice()


def MenuChoice():
    """
    Affiche le menu des fonctionnalités ainsi que les résultats souhaités
    """
    choice = int(input("Veuillez choisir une option : "))
    while choice < 0 or choice > 5:
        print("Veuillez choisir un nombre entre 1 et 5")
        choice = int(input("Quel est votre choix ? "))

    if choice == 1:
        print("Les mots les moins importants sont :",
              LessImportantWords(list_of_export(list_of_files("./cleaned/", "txt"))))
        print()
        response = str(input("Continuer ? Y/N"))
        if response == "y" or "Y" or "yes":
            Menu()
        else:
            MainMenu()

    elif choice == 2:
        print("Le(s) mot(s) ayant le score TF-IDF le plus élevé est :",
              MaxTFIDFWords(list_of_export(list_of_files("./cleaned/", "txt"))))
        print()
        response = str(input("Continuer ? Y/N"))
        if response == "y" or "Y" or "yes":
            Menu()
        else:
            MainMenu()

    elif choice == 3:
        print("Le(s) mot(s) le(s) plus répété(s) par Chirac est :",
              MostRepeatedWords(list_of_files("./speeches/", "txt"), "Chirac"))
        print()
        response = str(input("Continuer ? Y/N"))
        if response == "y" or "Y" or "yes":
            Menu()
        else:
            MainMenu()

    elif choice == 4:
        print(SearchWord("nation", True))
        print()
        response = str(input("Continuer ? Y/N"))
        if response == "Y" or "Y" or "yes":
            Menu()
        else:
            MainMenu()

    elif choice == 5:
        print(SearchWord("climat", False))
        print()
        response = str(input("Continuer ? Y/N"))
        if response == "Y" or "Y" or "yes":
            Menu()
        else:
            MainMenu()

    elif choice == 0:
        MainMenu()


def TokenizeQuestion(question):
    """
    :param question: la question à tokenizer
    :return: la question tokenizée
    """
    characters_to_remove = {'"': ' ', ',': ' ', '-': ' ', '.': ' ', "'": ' ', '!': ' ', ':': ' ', ';': ' ', '`': ' ',
                            '?': ' '}
    cleaned_text = ''.join(characters_to_remove.get(char, char) for char in question)
    cleaned_text = cleaned_text.lower()
    return cleaned_text.split()


def SearchTokenizeQuestionInMatrix(question, list_export):
    """
    :param question: la question à tokenizer
    :param list_export: liste des fichiers dans le répertoire cleaned
    :return: la matrice tf idf de la question
    """
    matrix = TFIDFMatrix(list_export)
    question = TokenizeQuestion(question)
    matrix_question = {}
    for word in question:
        if word in matrix:
            matrix_question[word] = matrix[word]
    return matrix_question


def TFIDFMatrixDocsByWords(list_export):
    """
    :param list_export: liste des fichiers dans le répertoire cleaned
    :return: la matrice idf des mots dans les documents
    """
    matrix = []
    for word, values in TFIDFMatrix(list_export).items():
        matrix.append(values)
    matrix_tf_idf = [list(row) for row in zip(*matrix)]

    return matrix_tf_idf


def TFOfAQuestion(question, list_export):
    """
    :param question_tokens: la question à tokenizer
    :return: le tf de la question
    """
    tf_corpus = TermFrequencyTotal(list_export)
    question_tokens = TokenizeQuestion(question)
    tf = {}
    for word in question_tokens:
        if word not in tf:
            tf[word] = 1
        else:
            tf[word] += 1
    for word, val in tf.items():
        tf[word] /= len(question_tokens)

    for word in tf_corpus:
        if word not in tf.keys():
            tf_corpus[word] = 0
        elif word in tf.keys():
            tf_corpus[word] = tf[word]
    return tf_corpus


def TFIDFVectorQuestion(dict_tf, dict_idf, question):
    tf_idf_vector = []
    dict_tf_question = dict_tf
    dict_idf_total = dict_idf
    question_tokens = TokenizeQuestion(question)

    for word, score_idf in dict_idf_total.items():
        if word in question_tokens:
            tf_idf_vector.append(dict_tf_question[word] * score_idf)
        else:
            tf_idf_vector.append(0)
    return tf_idf_vector


def WordOfTFIDFVectorQuestion(dict_tf, dict_idf, question):
    dict_tf_question = dict_tf
    dict_idf_total = dict_idf
    question_tokens = TokenizeQuestion(question)
    word_dict = {}
    max_word = ""

    for word, score_idf in dict_idf_total.items():
        if word in question_tokens:
            word_dict[word] = dict_tf_question[word] * score_idf
        else:
            word_dict[word] = 0

    for word, score in word_dict.items():
        if score == max(word_dict.values()):
            max_word = word

    return max_word


def ScalarProduct(dict_a, dict_b):
    product_ab = 0
    for file in range(len(dict_a)):
        product_ab += dict_a[file] * dict_b[file]
    return product_ab


def VectorNorm(vector):
    norm = 0
    for val in vector:
        norm += val ** 2
    norm = sqrt(norm)
    return norm


def Similarity(vector_a, vector_b):
    product_ab = ScalarProduct(vector_a, vector_b)
    norm_a = VectorNorm(vector_a)
    norm_b = VectorNorm(vector_b)
    sum_norm_ab = norm_a * norm_b
    if sum_norm_ab != 0:
        result = product_ab / sum_norm_ab
    else:
        result = 0
    return result


def DocumentPertinence(vector_question, list_export):
    """
    :param vector_question: la matrice tf idf de la question
    :param list_export: liste des fichiers dans le répertoire cleaned
    :return: le fichier le plus pertinent
    """
    matrix = TFIDFMatrixDocsByWords(list_export)
    list_of_scores = []

    for i in range(len(matrix)):
        list_of_scores.append(Similarity(vector_question, matrix[i]))

    most_pertinent = list_export[list_of_scores.index(max(list_of_scores))]
    return FileEquivalentInSpeeches(most_pertinent)


def FileEquivalentInSpeeches(searched_file):
    searching_file = searched_file[10:]
    for file in listdir("./speeches"):
        if file == searching_file:
            return "./speeches/" + file


def MaxTFIDFVectorQuestion(vector_question):
    for score in vector_question:
        if score == max(vector_question):
            return score


def SentenceOfQuestion(question_vector, dict_tf, dict_idf, question):
    file = DocumentPertinence(question_vector, list_of_export(list_of_files("./cleaned/", "txt")))
    text = open_file(file).split(".")
    word = WordOfTFIDFVectorQuestion(dict_tf, dict_idf, question)
    for sentence in text:
        if word in sentence:
            return sentence


def ResponseOfQuestion(question):
    question_words = TokenizeQuestion(question)
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr!"
    }

    for word in question_words:
        if word in question_starters:
            return question_starters[word]
        else:
            return "Voici votre réponse :"


if __name__ == "__main__":
    print("Please run the main file instead.")
