# build_index.py
import os
import json
import glob
from tqdm import tqdm
import faiss
import pickle
from sentence_transformers import SentenceTransformer

INDEX_DIR = "data/faiss_index"
DISCOURSE_FILE = "discourse_posts.json"
COURSE_DIR = "markdown_files"

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_course_chunks():
    chunks = []
    for md_file in glob.glob(os.path.join(COURSE_DIR, "*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            text = f.read()
            filename = os.path.basename(md_file)
            for para in text.split("\n\n"):
                if len(para.strip()) > 50:
                    chunks.append({
                        "text": para.strip(),
                        "source": filename
                    })
    return chunks

def load_forum_chunks():
    with open(DISCOURSE_FILE, "r") as f:
        posts = json.load(f)
    return [
        {
            "text": post["content"],
            "source": post["url"]
        }
        for post in posts if len(post["content"]) > 50
    ]

def main():
    os.makedirs(INDEX_DIR, exist_ok=True)
    all_chunks = load_course_chunks() + load_forum_chunks()
    print(f"📚 Loaded {len(all_chunks)} total text chunks")

    texts = [chunk["text"] for chunk in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)

    faiss.write_index(index, os.path.join(INDEX_DIR, "index.faiss"))
    with open(os.path.join(INDEX_DIR, "sources.pkl"), "wb") as f:
        pickle.dump(all_chunks, f)

    print("✅ Index saved in data/faiss_index")

if __name__ == "__main__":
    main()
