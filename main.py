from function import (
    list_of_files,
    clean_all_files,
    list_of_import,
    list_of_export,
    MainMenu)

SPEECHES_DIRECTORY_LIST = "./speeches/"
CLEANED_DIRECTORY = "./cleaned/"

speechesNominationList = list_of_files(SPEECHES_DIRECTORY_LIST, "txt")
cleanedNominationList = list_of_files(CLEANED_DIRECTORY, "txt")

list_import = list_of_import(speechesNominationList)
list_export = list_of_export(cleanedNominationList)

clean_all_files(list_import, list_export)
if __name__ == "__main__":
    MainMenu()

