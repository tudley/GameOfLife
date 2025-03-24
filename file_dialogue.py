from tkinter import *
from tkinter import filedialog
import json

def open_file_dialogue():
    filepath = filedialog.askopenfilename(initialdir= "/python_learning/personalProjects/PythonProjects/game_of_life/files",
                                          title= "Select a file to import:",
                                          filetypes=(("JSON Files", "*.json"),))
    return filepath

def load_json_file(filepath):
    if filepath:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data
    else:
        return None
    