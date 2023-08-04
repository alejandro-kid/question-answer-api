import fitz
import os

from flask import Response, current_app, json
from src.initializer import doc_context
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import GPT4AllEmbeddings
from langchain.chains.question_answering import load_qa_chain


def process_files(document):
    try:
        #clear context
        global doc_context
        doc_context = ""

        temp_file = os.path.join(get_temp_folder(), document.filename)
        document.save(temp_file)

        doc =  fitz.open(temp_file)
        n = doc.page_count
        for i in range(0, n):
            page = doc.load_page(i)
            page_text = page.get_text("text")
            doc_context += doc_context + page_text

        delete_file(temp_file)
        data = {
                "success": True,
                "message": "Document processed successfully"
        }
        response = Response(json.dumps(data), 200, mimetype='application/json')
    except Exception as e:
        response = Response(e, 500, mimetype='application/json')
    return response

def get_temp_folder() -> str:
    dir = current_app.root_path + "/temp"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    return dir

def delete_file(path:str) -> None:
    
    if os.path.exists(path):
        os.remove(path)
