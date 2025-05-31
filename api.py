# api.py
import os
import pickle
import faiss
from fastapi import FastAPI, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

model = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_PATH = "data/faiss_index/index.faiss"
SOURCES_PATH = "data/faiss_index/sources.pkl"

print("🔍 Loading index and sources...")
index = faiss.read_index(INDEX_PATH)
with open(SOURCES_PATH, "rb") as f:
    sources = pickle.load(f)
print("✅ Ready to answer questions!")

@app.post("/api/")
def answer_query(query: Query):
    q_embedding = model.encode([query.question])
    D, I = index.search(q_embedding, k=5)

    top_sources = [sources[i] for i in I[0]]
    response = {
        "answer": top_sources[0]["text"],
        "links": [
            {"url": src["source"], "text": src["source"]}
            for src in top_sources
        ]
    }
    return response
