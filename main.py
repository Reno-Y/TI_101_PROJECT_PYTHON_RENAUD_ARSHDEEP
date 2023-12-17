from function import (
    list_of_files,
    clean_all_files,
    list_of_import,
    list_of_export,
    main_menu,
    main_menu_choice,
    idf,
tf_idf_vector,
    tf_of_a_question,
    tf_total,
    Search_Tokenize_Question_in_matrix)

SPEECHES_DIRECTORY_LIST = "./speeches/"
CLEANED_DIRECTORY = "./cleaned/"

speechesNominationList = list_of_files(SPEECHES_DIRECTORY_LIST, "txt")
cleanedNominationList = list_of_files(CLEANED_DIRECTORY, "txt")

list_import = list_of_import(speechesNominationList)
list_export = list_of_export(cleanedNominationList)

clean_all_files(list_import, list_export)


question = str(input("Posez votre question : "))

print("tf of a question : ")

print(tf_of_a_question(question, list_export))

print()


print("Le tf idf vecteur")
print(tf_idf_vector(tf_of_a_question(question, list_export), idf(list_export), question))





"""
print(Search_Tokenize_Question_in_matrix(question, list_export))
"""

main_menu()

"""
question = str(input("Posez votre question : "))
print(Search_Tokenize_Question_matrix(question, list_export))
"""
"""
if __name__ == "__main__":
    menu()
    while True:
        menu_choice()
        print("\n")
"""
