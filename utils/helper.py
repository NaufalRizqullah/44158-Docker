from pathlib import Path

def load_class_names():

    file = "class_names.txt"
    path_file = Path("./src/data") / file

    with open(path_file,"r") as f:
        class_names = [item.strip() for item in f.readlines()]

    return class_names