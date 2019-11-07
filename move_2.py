import os, shutil 

PATH_FROM = "/home/marius/ntnu/master/Split-farge/"
PATH_TO = "/home/marius/ntnu/master/new2/"
PATH_LABELS = "/home/marius/ntnu/master/Split-farge/" 
names = []
def do():
    for file in os.listdir(PATH_LABELS):
        if file.endswith(".jpg"):
            continue
        name = file.split(".")
        name = name[0] + name[1]
        if name == "classes":
            continue
        for file_2 in os.listdir(PATH_FROM):
            name_2 = file_2.split(".")
            name_2 = name_2[0] + name_2[1]
            if name == name_2:
                names.append(file_2)
                full_path = PATH_FROM + file_2
                full_path_2 = PATH_LABELS + file
                shutil.copy(full_path, PATH_TO)
                shutil.copy(full_path_2, PATH_TO)





if __name__ == "__main__":
    do()
