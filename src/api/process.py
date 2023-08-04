import fitz
import os
from flask import Response, current_app
from src.initializer import doc_context

def process_files(document):

    # # clear context
    global doc_context
    doc_context = ""

    temp_file = os.path.join(get_temp_folder(), document.filename)
    document.save(temp_file)
    
    delete_file(temp_file)



def get_temp_folder() -> str:
    dir = current_app.root_path + "/temp"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    return dir

def delete_file(path:str) -> None:
    
    if os.path.exists(path):
        os.remove(path)