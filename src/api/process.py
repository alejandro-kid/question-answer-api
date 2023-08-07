import os
import fitz
from flask import Response, current_app, json
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import GPT4AllEmbeddings
from langchain.chains.question_answering import load_qa_chain

def process_files(document):
    try:
        temp_file = os.path.join(get_temp_folder(), document.filename)
        document.save(temp_file)

        data = {
                "success": True,
                "message": "Document processed successfully"
        }
        response = Response(json.dumps(data), 200, mimetype='application/json')
    except Exception as e:
        data = {
            "success": False,
            "error_message": str(e)
        }
        response = Response(json.dumps(data), 500, mimetype='application/json')
    return response

def query(query_text):
    try:

        doc = fitz.Document()
        if os.listdir(get_temp_folder()):
            doc.open(get_temp_folder() + "/" + os.listdir(get_temp_folder())[0])
        else:
            raise Exception("No document found")

        embeddings = GPT4AllEmbeddings()
        n = doc.page_count

        doc_content = ""
        for i in range(0, n):
            page_n = doc.load_page(i)
            page_content = page_n.get_text("text")
            doc_content += page_content + "\n"

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len
        )
        texts = text_splitter.split_text(doc_content)

        document_search = FAISS.from_texts(texts, embeddings)

        docs = document_search.similarity_search(query_text)

        full_text = [ doc.page_content for doc in docs]

        data = {
                "success": True,
                "message": "Query processed successfully",
                "full_text": full_text
        }
        response = Response(json.dumps(data), 200, mimetype='application/json')
    except Exception as e:
        data = {
            "success": False,
            "error_message": str(e)
        }
        response = Response(json.dumps(data), 500, mimetype='application/json')
    return response

def get_temp_folder() -> str:
    dir = current_app.root_path + "/temp"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    return dir

def delete_file(path:str) -> None:
    
    if os.path.exists(path):
        os.remove(path)
