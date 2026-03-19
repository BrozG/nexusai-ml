import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# load scraped data
with open("smit_raw_text.json","r",encoding="utf-8") as f:
    pages = json.load(f)

chunks = []
sources = []

chunk_size = 500
overlap = 50

for page in pages:

    url = page["url"]
    text = page["text"]

    words = text.split()

    for i in range(0,len(words),chunk_size-overlap):

        chunk_words = words[i:i+chunk_size]

        if len(chunk_words) < 50:
            continue

        chunk = " ".join(chunk_words)

        chunks.append(chunk)
        sources.append(url)

print("Total chunks:",len(chunks))

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")

embeddings = model.encode(chunks,show_progress_bar=True)

embeddings = np.array(embeddings).astype("float32")

# normalize for cosine similarity
faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

faiss.write_index(index,"education_vector.index")

print("Vector database saved.")

# metadata
metadata = []

for i in range(len(chunks)):

    metadata.append({
        "id":i,
        "text":chunks[i],
        "source_url":sources[i]
    })

with open("education_metadata.json","w",encoding="utf-8") as f:
    json.dump(metadata,f,indent=2)

print("Metadata saved.")