"""
Build the FAISS vector store from PDFs.

Usage:
    python ingest.py --pdf_dir ./pdfs --out ./vector_store
"""

import argparse
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def add_document_to_index(pdf_path: str, index_dir: str) -> int:
    """
    Load a single PDF, chunk it, and merge it into the FAISS index at
    index_dir. Creates the index if it doesn't exist yet. Returns the
    number of chunks added.
    """
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if os.path.exists(index_dir):
        vector_store = FAISS.load_local(
            index_dir, embeddings, allow_dangerous_deserialization=True
        )
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)

    vector_store.save_local(index_dir)
    return len(chunks)


def build_index(pdf_dir: str, out_dir: str):
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in {pdf_dir}")

    docs = []
    for fname in pdf_files:
        loader = PyPDFLoader(os.path.join(pdf_dir, fname))
        docs.extend(loader.load())
        print(f"Loaded {fname}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(out_dir)
    print(f"Saved FAISS index to {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_dir", default="./pdfs")
    parser.add_argument("--out", default="./vector_store")
    args = parser.parse_args()
    build_index(args.pdf_dir, args.out)