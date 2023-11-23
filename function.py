import os 


def list_of_files(directory, extension):

    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names



def cleaning_chirac1():
   with open("./speeches/Nomination_Chirac1.txt",'r') as f1 , open("./cleaned/Nomination_Chirac1_cleaned.txt",'w') as f2:
       for line in f1 : 
           f2.write(line)
























""" def copy_discours(list_discours, copy_folder):

    if not os.path.exists(copy_folder):
        os.makedirs(copy_folder)


    for file_path in list_discours :
        #on sépare le nom des fichiers de leurs extension et nom afin de pouvoir ajouter "cleaned" à la fin
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        #on rajoute cleaned à la fin du fichier
        new_file_name = f"{file_name}_cleaned{file_extension}"
        #on indique la destination du fichier
        destination_path = os.path.join(copy_folder, new_file_name)
        #on copie le fichier
        shutil.copy(file_path, destination_path)
"""
