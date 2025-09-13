# -------------------------
# 📁 agent/embedder.py
# -------------------------
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os

def embed_text_chunks(chunks, source_name, persist_dir="vector_db"):
    os.makedirs(persist_dir, exist_ok=True)
    docs = [Document(page_content=chunk, metadata={"source": source_name}) for chunk in chunks]
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma.from_documents(docs, embedder, persist_directory=persist_dir)
