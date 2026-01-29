# RAG-Based Question Answering System

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** based Question Answering system.  
Users can upload documents and ask questions, and the system returns answers grounded strictly in the uploaded content.

The system is built using **FastAPI**, **semantic embeddings**, **FAISS vector search**, and a **background ingestion pipeline**, focusing on clarity and explainability rather than heavy frameworks.

---

## Key Features
- Supports **PDF** and **TXT** document uploads
- Automatic document **chunking and embedding**
- Vector storage using **FAISS**
- **Similarity-based retrieval** of relevant chunks
- Background job for document ingestion
- Request validation using **Pydantic**
- Basic in-memory **rate limiting**
- Lightweight frontend for interaction

---

## Technology Stack
- **Python**
- **FastAPI** – API framework
- **SentenceTransformers** – Embedding generation
- **FAISS** – Vector similarity search
- **PyPDF2** – PDF parsing
- **NumPy** – Data handling

---

## Project Structure
rag-project/
│
├── rag_api.py # FastAPI backend
│
├── static/ # Frontend files
│ ├── index.html
│ ├── style.css
│ └── app.js
│
├── data/
│ ├── documents/ # Uploaded documents
│ └── index/ # FAISS index + metadata
│
├── README.md
└── MANDATORY_EXPLANATION.md  

---

## Architecture Diagram
+-------------------+
| Client / Browser |
+-------------------+
|
v
+-------------------+
| FastAPI Server |
| (rag_api.py) |
+-------------------+
|
+--------------------+
| |
v v
+-------------------+ +-------------------+
| Document Upload | | Query API |
| (/upload) | | (/query) |
+-------------------+ +-------------------+
| |
v v
+-------------------+ +-------------------+
| Background Task | | Question Embedding|
| (Ingestion) | +-------------------+
+-------------------+ |
| v
v +-------------------+
+-------------------+ | Similarity Search |
| Chunking + | | (FAISS) |
| Embedding | +-------------------+
+-------------------+ |
| v
v +-------------------+
+-------------------+ | Retrieved Chunks |
| FAISS Vector DB | +-------------------+
+-------------------+ |
v
+-------------------+
| Answer Generation |
+-------------------+
|
v
+-------------------+
| API Response |
+-------------------+


---

## How the System Works

1. **Document Upload**
   - User uploads a PDF or TXT file
   - File is saved locally
   - Background task starts ingestion

2. **Ingestion Pipeline**
   - Document is read and split into chunks
   - Each chunk is converted into an embedding
   - Embeddings are stored in FAISS

3. **Query Flow**
   - User submits a question
   - Question is embedded
   - FAISS retrieves top-k similar chunks
   - Retrieved content is used to generate an answer

---

## API Endpoints

### Upload DocumentPOST /upload

- Accepts PDF or TXT files
- Triggers background ingestion


### Query Document

POST /query



Request body:
  ```json
  {
    "question": "What is the main topic of the document?",
    "top_k": 5
  }
  
  Response:
  
  {
    "answer": "Generated answer based on document content",
    "sources": ["example.pdf"]
  }
  Health Check
  GET /health
  Setup Instructions
  1. Install Dependencies
  pip install fastapi uvicorn pydantic sentence-transformers faiss-cpu python-multipart PyPDF2 numpy
  2. Run the Application
  python rag_api.py
  3. Open the Application
  http://127.0.0.1:8000/
  Design Choices
  
  FAISS was chosen for its speed and simplicity in local vector search
  
  BackgroundTasks allow non-blocking ingestion
  
  No heavy RAG frameworks were used to keep the system transparent
  
  Chunking and retrieval logic are explicitly implemented
  
  Known Limitations
  
  Similarity-based retrieval may miss answers spread across multiple distant chunks
  
  In-memory rate limiting is not persistent
  
  Retrieval quality depends on embedding performance
  
  Future Enhancements
  
  Add cross-chunk re-ranking
  
  Integrate a full LLM-based generation step
  
  Cache embeddings for faster queries
  
  Add confidence scores and citations per answer
  
  Author Notes
  
  This project was built to demonstrate practical understanding of RAG systems, vector search, and API-based AI system design, with emphasis on explainability and clean architecture.
  
  
  
  ---
  
  
  ### ✅ This README:
  - Meets **all task requirements**
  - Looks **professional on GitHub**
  - Is **easy for evaluators to follow**
  - Clearly explains architecture, flow, and design choices
  
  
  If you want next, I can:
  - Review your **GitHub repo like an evaluator**
  - Convert the diagram into **draw.io format**
  - Write a **submission cover note**
  - Prepare **viva / interview questions & answers**
  ::contentReference[oaicite:0]{index=0}
