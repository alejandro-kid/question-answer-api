import chromadb
from flask import current_app

client = chromadb.PersistentClient(path=current_app.root_path + "/chromadb")