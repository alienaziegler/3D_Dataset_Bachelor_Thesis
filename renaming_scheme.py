import os
import re

# Path and globals
directory = r"/home/aliena/Uni/Bachelor_Arbeit/AlgoEval1/Geschlinge1_Result"
file_prefix = "left_"
file_type = ".ply"

def rename_files(directory):

    # collect relevant files in wrong order
    files = []
    for file_name in os.listdir(directory):
        if file_name.endswith(file_type):
            files.append(file_name)
    files.sort()
    if len(files) > 99:
        raise IndexError("WARNING! This script supports up to 100 relevant files.")
    
    # replace with correct order, use nleft_ to avoid name collision
    for pos, file_name in enumerate(files):

        wrong_file_name = f'{file_prefix}{pos}{file_type}'
        print(f"{wrong_file_name} --> {file_name}")

        old_path = os.path.join(directory, wrong_file_name)
        new_path = os.path.join(directory, f"n{file_name}")
        os.rename(old_path, new_path)

    # replace nleft_ with left_
    for file_name in os.listdir(directory):
        new_file_name = file_name
        if file_name.startswith(f"n{file_prefix}"):
            new_file_name = file_name[1:]

        if re.search(f'{file_prefix}[0-9]{file_type}', new_file_name):
            index = int(new_file_name[-(len(file_type)+1)])
            new_file_name = f'{file_prefix}{index:02d}{file_type}'

        old_path = os.path.join(directory, file_name)
        new_path = os.path.join(directory, new_file_name)
        os.rename(old_path, new_path)
            
    

if __name__ == "__main__":
    renamed_files = rename_files(directory)
    print("Files renamed successfully.")
