# search_api.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_methods=["*"],
    allow_headers=["*"],
)

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load everything
index = faiss.read_index("data/index.faiss")
vectors = np.load("data/vectors.npy")
with open("data/metadata.json") as f:
    metadata = json.load(f)

from fastapi.responses import JSONResponse  # ✅ needed import

class BookItem(BaseModel):
    title: str
    reason: str
    source_url: str

class SearchResponse(BaseModel):
    books: list[BookItem]

@app.get("/search", response_model=SearchResponse)
def search_books(q: str):
    query_vec = model.encode(q, normalize_embeddings=True).reshape(1, -1)
    D, I = index.search(query_vec, k=10)  # broader context

    book_map = {}  # title → info dict

    for i in I[0]:
        if i >= len(metadata):
            continue

        post = metadata[i]
        url = post.get("url", "")
        comments = post.get("comments", [])
        body = post.get("body", "")

        for book in post.get("books", []):
            if book in book_map:
                continue  # avoid duplicates

            # Try to find a relevant comment mentioning the book
            reason = next(
                (c for c in comments if book.lower() in c.lower()),
                None
            )

            # Fallback if no matching comment
            reason = reason or body[:300]

            book_map[book] = {
                "title": book,
                "reason": reason.strip(),
                "source_url": url
            }

    return JSONResponse(content={"books": list(book_map.values())[:5]})