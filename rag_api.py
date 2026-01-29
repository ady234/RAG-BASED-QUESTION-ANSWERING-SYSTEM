import os
import time
import uuid
import numpy as np
import faiss

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# =========================
# Configuration
# =========================

DATA_DIR = "data"
DOC_DIR = os.path.join(DATA_DIR, "documents")
INDEX_DIR = os.path.join(DATA_DIR, "index")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

RATE_LIMIT = 10
RATE_WINDOW = 60  # seconds

EMBEDDING_DIM = 384

INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
META_PATH = os.path.join(INDEX_DIR, "meta.npy")

os.makedirs(DOC_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# =========================
# FastAPI App
# =========================

app = FastAPI(title="RAG-Based Question Answering API")

# Serve static files correctly
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# Embedding Model
# =========================

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# Pydantic Models
# =========================

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=10)

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# =========================
# Rate Limiting
# =========================

clients = {}

def check_rate_limit(client_ip: str):
    now = time.time()
    window_start = now - RATE_WINDOW

    timestamps = clients.get(client_ip, [])
    timestamps = [t for t in timestamps if t > window_start]

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    timestamps.append(now)
    clients[client_ip] = timestamps

# =========================
# FAISS Helpers
# =========================

def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return faiss.IndexFlatIP(EMBEDDING_DIM)

def load_meta():
    if os.path.exists(META_PATH):
        return np.load(META_PATH, allow_pickle=True).tolist()
    return []

def save_index(index):
    faiss.write_index(index, INDEX_PATH)

def save_meta(meta):
    np.save(META_PATH, meta)

# =========================
# Document Processing
# =========================

def read_document(path: str) -> str:
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

def chunk_text(text: str):
    words = text.split()
    chunks = []
    step = CHUNK_SIZE - CHUNK_OVERLAP

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + CHUNK_SIZE])
        if chunk.strip():
            chunks.append(chunk)

    return chunks

def ingest_document(file_path: str):
    index = load_index()
    meta = load_meta()

    text = read_document(file_path)
    chunks = chunk_text(text)

    if not chunks:
        return

    embeddings = embedder.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    index.add(embeddings)

    for chunk in chunks:
        meta.append({
            "id": str(uuid.uuid4()),
            "text": chunk,
            "source": os.path.basename(file_path)
        })

    save_index(index)
    save_meta(meta)

# =========================
# Retrieval & Answering
# =========================

def retrieve_chunks(question: str, top_k: int):
    if not os.path.exists(INDEX_PATH):
        return []

    index = faiss.read_index(INDEX_PATH)
    meta = load_meta()

    q_embedding = embedder.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(q_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(meta):
            results.append(meta[idx])

    return results

def generate_answer(question: str, contexts: list[str]) -> str:
    if not contexts:
        return "The answer is not found in the uploaded documents."

    combined_context = " ".join(contexts)
    return f"Based on the document content:\n\n{combined_context[:800]}"

# =========================
# Routes
# =========================

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    file_path = os.path.join(DOC_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(ingest_document, file_path)

    return {"status": "uploaded", "file": file.filename}

@app.post("/query", response_model=QueryResponse)
async def query_document(request: Request, query: QueryRequest):
    check_rate_limit(request.client.host)

    results = retrieve_chunks(query.question, query.top_k)
    contexts = [r["text"] for r in results]
    sources = list(set(r["source"] for r in results))

    answer = generate_answer(query.question, contexts)

    return QueryResponse(answer=answer, sources=sources)

@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# Entry Point
# =========================

if __name__ == "__main__":
    import uvicorn
    print("Starting RAG API server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")