# embed.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

posts = []
embeddings = []

with open("data/posts.jsonl") as f:
    for line in f:
        post = json.loads(line)
        text = post["title"] + " " + post["body"]
        emb = model.encode(text, normalize_embeddings=True)
        embeddings.append(emb)
        posts.append({
            "query": text,
            "books": post["suggested_books"],
            "id": post["id"],
            "score": post["score"]
        })

# Save vectors
vectors = np.stack(embeddings)
np.save("data/vectors.npy", vectors)

# Save metadata
with open("data/metadata.json", "w") as f:
    json.dump(posts, f, indent=2)

# Create FAISS index
index = faiss.IndexFlatIP(vectors.shape[1])  # cosine similarity (normalized)
index.add(vectors)
faiss.write_index(index, "data/index.faiss")

print(f"✅ Indexed {len(posts)} queries.")
