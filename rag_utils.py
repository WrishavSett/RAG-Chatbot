import os
import faiss
import numpy as np
from typing import List
from PyPDF2 import PdfReader
from docx import Document
import requests
import tiktoken

def parse_txt(file):
    return file.read().decode("utf-8")

def parse_pdf(file):
    reader = PdfReader(file)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def parse_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(file):
    if file.name.endswith(".pdf"):
        return parse_pdf(file)
    elif file.name.endswith(".docx"):
        return parse_docx(file)
    elif file.name.endswith(".txt"):
        return parse_txt(file)
    else:
        return ""

def chunk_text(text, max_tokens=500):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    words = text.split()
    chunks, chunk = [], []

    for word in words:
        chunk.append(word)
        if len(tokenizer.encode(" ".join(chunk))) > max_tokens:
            chunks.append(" ".join(chunk))
            chunk = []
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

# --- 🔄 LOCAL EMBEDDING VIA OLLAMA ---
def get_embedding(text: str, model: str = "nomic-embed-text") -> List[float]:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    if response.status_code == 200:
        return response.json()["embedding"]
    else:
        raise Exception(f"Ollama embedding error: {response.text}")

def create_vector_store(chunks: List[str]):
    embeddings = [get_embedding(chunk) for chunk in chunks]
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index, chunks

def search_similar_chunks(query, index, chunks, top_k=3):
    query_embedding = get_embedding(query)
    D, I = index.search(np.array([query_embedding]).astype("float32"), top_k)
    return [chunks[i] for i in I[0]]