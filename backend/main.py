import os
import shutil
import uuid

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import AgenticRAG
from ingest import add_document_to_index

UPLOAD_ROOT = "./uploads"
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./vector_store")

app = FastAPI(title="Agentic RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag: AgenticRAG | None = None


@app.on_event("startup")
def load_rag():
    global rag
    os.makedirs(UPLOAD_ROOT, exist_ok=True)
    rag = AgenticRAG()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    trace: list[dict]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if rag is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized yet.")
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    return rag.run(req.query)


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    folder: str
    chunks_added: int


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    doc_id = uuid.uuid4().hex[:12]
    doc_folder = os.path.join(UPLOAD_ROOT, doc_id)
    os.makedirs(doc_folder, exist_ok=True)

    dest_path = os.path.join(doc_folder, file.filename)
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        num_chunks = add_document_to_index(dest_path, FAISS_INDEX_PATH)
    except Exception as e:
        shutil.rmtree(doc_folder, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {e}")

    if rag is not None:
        rag.reload_vector_store()

    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        folder=doc_folder,
        chunks_added=num_chunks,
    )


@app.get("/health")
def health():
    return {"status": "ok", "ready": rag is not None}