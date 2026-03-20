import json
import os

def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            content = f.read()
        return content
    
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found")
        return None
    
def save_results(result_dic, filepath):
    directory =  os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filepath, "w") as f:
        json.dump(result_dic, f, indent=4)