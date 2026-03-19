import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="SMIT AI Assistant")

st.title("🎓 SMIT AI Assistant")
st.write("Ask questions about Sikkim Manipal Institute of Technology")

# load metadata
with open("education_metadata.json","r",encoding="utf-8") as f:
    metadata = json.load(f)

# load vector index
index = faiss.read_index("education_vector.index")

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query,k=3):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    faiss.normalize_L2(query_embedding)

    D,I = index.search(query_embedding,k)

    results = []

    for i in I[0]:
        results.append(metadata[i])

    return results


query = st.text_input("Ask your question")

if query:

    results = search(query)

    st.subheader("Top Results")

    for i,r in enumerate(results):

        st.markdown(f"### Result {i+1}")

        st.write(r["text"][:400] + "...")

        st.markdown(f"**Source:** {r['source_url']}")

        st.markdown("---")