from function import (
    list_of_files,
    clean_all_files,
    list_of_import,
    list_of_export,
    MainMenu,
    main_menu_choice,
    InverseDocumentFrequency,
    TFIDF,
    TFIDFVectorQuestion,
    TFOfAQuestion,
    DocumentPertinence,
    MaxTFIDFVectorQuestion,
    SentenceOfQuestion)

SPEECHES_DIRECTORY_LIST = "./speeches/"
CLEANED_DIRECTORY = "./cleaned/"

speechesNominationList = list_of_files(SPEECHES_DIRECTORY_LIST, "txt")
cleanedNominationList = list_of_files(CLEANED_DIRECTORY, "txt")

list_import = list_of_import(speechesNominationList)
list_export = list_of_export(cleanedNominationList)

clean_all_files(list_import, list_export)

question = str(input("Posez votre question : "))

print(TFOfAQuestion(question, list_export))

print("Le tf idf vecteur")
vector_question = TFIDFVectorQuestion(TFOfAQuestion(question, list_export), InverseDocumentFrequency(list_export), question)
matrix_tf_idf = TFIDF(list_export)

print(DocumentPertinence(vector_question, list_export))
print()
print(MaxTFIDFVectorQuestion(vector_question))
print()
print(SentenceOfQuestion(vector_question))

