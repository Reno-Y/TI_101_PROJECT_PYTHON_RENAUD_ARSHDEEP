from function import (
    list_of_files,
    clean_all_files,
    list_of_import,
    list_of_export,
    main_menu,
    main_menu_choice,
    idf,
    tf_idf,
    tf_idf_vector_question,
    tf_of_a_question,
    document_pertinence,
max_tf_idf_vector_question)

SPEECHES_DIRECTORY_LIST = "./speeches/"
CLEANED_DIRECTORY = "./cleaned/"

speechesNominationList = list_of_files(SPEECHES_DIRECTORY_LIST, "txt")
cleanedNominationList = list_of_files(CLEANED_DIRECTORY, "txt")

list_import = list_of_import(speechesNominationList)
list_export = list_of_export(cleanedNominationList)

clean_all_files(list_import, list_export)


question = str(input("Posez votre question : "))



print("Le tf idf vecteur")
vector_question = tf_idf_vector_question(tf_of_a_question(question, list_export), idf(list_export), question)
matrix_tf_idf = tf_idf(list_export)

print(document_pertinence(vector_question, list_export))
print()
print(max_tf_idf_vector_question(vector_question))


main_menu()


