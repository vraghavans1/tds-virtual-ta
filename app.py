from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import pickle

app = FastAPI()

class Query(BaseModel):
    question: str

model = None
index = None
sources = None

def load_index():
    global model, index, sources
    if model is None:
        print("🔍 Loading embedding model and FAISS index...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        index = faiss.read_index("data/faiss_index/index.faiss")
        with open("data/faiss_index/sources.pkl", "rb") as f:
            sources = pickle.load(f)
        print("✅ Index ready.")

@app.post("/api/")
def answer_query(query: Query):
    load_index()
    q_embed = model.encode([query.question])
    D, I = index.search(q_embed, k=5)
    top_sources = [sources[i] for i in I[0]]
    return {
        "answer": top_sources[0]["text"],
        "links": [{"url": s["source"], "text": s["source"]} for s in top_sources]
    }
