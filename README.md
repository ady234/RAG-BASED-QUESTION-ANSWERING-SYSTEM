# RAG-BASED-QUESTION-ANSWERING-SYSTEM
API THAT ALLOWS USERS TO UPLOAD DOCUMENTS AND ASK QUESTIONS BASED ON THOSE DOCUMENTS USING A RETRIEVAL AUGMENTED GENERATION (RAG) APPROACH
RAG-Based Question Answering System
Overview

This project implements a Retrieval-Augmented Generation (RAG) based Question Answering system that allows users to upload documents and ask questions grounded in the uploaded content. The system combines semantic embeddings, vector similarity search, and answer generation to provide document-aware responses.

Features

Supports PDF and TXT document uploads

Automatic document chunking and embedding

Vector storage using FAISS

Similarity-based retrieval of relevant document chunks

Background document ingestion

API-based question answering

Basic rate limiting

Lightweight frontend for interaction

Tech Stack

FastAPI – API framework

SentenceTransformers – Embedding generation

FAISS – Vector similarity search

PyPDF2 – PDF parsing

Python – Core implementation

Project Structure
rag-project/
│
├── rag_api.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── data/
│   ├── documents/
│   └── index/
├── README.md
├── MANDATORY_EXPLANATION.md
Setup Instructions

Clone the repository

git clone <your-github-repo-url>
cd rag-project

Install dependencies

pip install fastapi uvicorn pydantic sentence-transformers faiss-cpu python-multipart PyPDF2 numpy

Run the application

python rag_api.py

Open in browser

http://127.0.0.1:8000/
API Endpoints
Upload Document
POST /upload

Accepts PDF or TXT files

Triggers background ingestion

Query Document
POST /query

Request body:

{
  "question": "Your question here",
  "top_k": 5
}

Response:

{
  "answer": "Generated answer",
  "sources": ["document_name"]
}
Known Limitations

Retrieval is based on top-k similarity and may miss distributed answers

Current generation step uses retrieved context directly (see explanation document)

No authentication or persistent rate-limit storage

Future Improvements

Add cross-chunk re-ranking

Integrate a full LLM generation step

Improve latency through embedding caching

Add answer confidence scores
