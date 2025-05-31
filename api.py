import os
import pickle
import faiss
import base64
from fastapi import FastAPI
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
    image: str | None = None  # Optional base64 image input

model = None
index = None
sources = None

INDEX_PATH = "data/faiss_index/index.faiss"
SOURCES_PATH = "data/faiss_index/sources.pkl"

# Load index only on first use
def load_index():
    global model, index, sources
    if model is None:
        print("🔍 Loading embedding model and FAISS index...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        index = faiss.read_index(INDEX_PATH)
        with open(SOURCES_PATH, "rb") as f:
            sources = pickle.load(f)
        print("✅ Index ready.")

@app.post("/api/")
def answer_query(query: Query):
    load_index()
    full_query = query.question

    # Optional: log image presence
    if query.image:
        try:
            image_data = base64.b64decode(query.image)
            print(f"🖼️ Received image of size: {len(image_data)} bytes")
            # Optionally save the image
            with open("received_image.webp", "wb") as f:
                f.write(image_data)
        except Exception as e:
            print(f"⚠️ Error decoding image: {e}")

    # Embed and retrieve from index
    q_embedding = model.encode([full_query])
    D, I = index.search(q_embedding, k=5)
    top_sources = [sources[i] for i in I[0]]

    response = {
        "answer": top_sources[0]["text"],
        "links": [
            {"url": s["source"], "text": s["source"]}
            for s in top_sources
        ]
    }
    return response
