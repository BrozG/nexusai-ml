import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -------------------------
# Load metadata
# -------------------------
with open("education_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# -------------------------
# Load FAISS index
# -------------------------
index = faiss.read_index("education_vector.index")

# -------------------------
# Load embedding model
# -------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# Search function
# -------------------------
def search(query, k=3):

    # convert query to embedding
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # search in FAISS index
    D, I = index.search(query_embedding, k)

    results = []

    for i in I[0]:
        results.append(metadata[i])   # return full metadata

    return results

# -------------------------
# Ask user question
# -------------------------
query = input("Enter your question: ")

results = search(query)

print("\nTop Results:\n")

# -------------------------
# Display results
# -------------------------
for r in results:

    print("\nResult:\n")
    print(r["text"])

    print("\nSource:", r["source_url"])

    print("\n------------------------")