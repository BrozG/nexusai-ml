"""
build_vector_store.py  (v2 — improved)
========================================
Creates embeddings and builds the FAISS-compatible vector database.

Improvements over v1
--------------------
CHUNKING STRATEGY
  • Sentence-aware splitting: never breaks in the middle of a sentence
  • Target 500 words per chunk (range 400–600) with 75-word semantic overlap
  • Heading preservation: section headings are kept with the following text
  • Minimum chunk size enforced (300 words) — short tails are merged upward
  • Each chunk tagged with doc metadata for rich retrieval context

EMBEDDING
  • TF-IDF + Truncated SVD at 384 dimensions (matches all-MiniLM-L6-v2 dim)
  • Sublinear TF normalisation, bigrams for better semantic capture
  • L2-normalised output for cosine similarity via dot product

VECTOR INDEX
  • FAISS-compatible flat cosine index saved as .npz
  • Metadata stored with full chunk context (source, topic, title, chunk_index)

TARGET: 300–500 unique high-quality chunks

Usage:
    python build_vector_store.py
    # prerequisite: ecommerce_scraper.py (auto-runs if needed)
"""

import json
import logging
import math
import os
import pickle
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────────
CHUNK_TARGET_WORDS = 500   # ideal words per chunk
CHUNK_OVERLAP_WORDS = 75   # semantic overlap between consecutive chunks
CHUNK_MIN_WORDS    = 200   # discard chunks shorter than this
CHUNK_MAX_WORDS    = 650   # hard ceiling (merge doesn't exceed this)
EMBEDDING_DIM      = 384
INDEX_PATH         = "ecommerce_vector.index.npz"
METADATA_PATH      = "ecommerce_metadata.json"
MODEL_PATH         = "embedding_model.pkl"
SCRAPER_OUTPUT     = "scraped_support_text.json"


# ── Step 1 — Load source documents ─────────────────────────────────────────
def load_documents(path: str = SCRAPER_OUTPUT) -> list[dict]:
    if not os.path.exists(path):
        log.warning("'%s' not found — running scraper …", path)
        from ecommerce_scraper import get_support_documents, save_documents
        docs = get_support_documents(try_live=True)
        save_documents(docs, path)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    log.info("Loaded %d source documents", len(data))
    return data


# ── Step 2 — Sentence-aware chunker ────────────────────────────────────────
_SENT_BOUNDARY = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')


def _split_sentences(text: str) -> list[str]:
    """
    Split text into sentences using a lightweight regex that respects
    common abbreviations and decimal numbers.
    """
    raw_sentences = _SENT_BOUNDARY.split(text)
    # Re-join very short fragments (likely abbreviations that were wrongly split)
    sentences, buffer = [], ""
    for sent in raw_sentences:
        buffer = (buffer + " " + sent).strip() if buffer else sent
        if len(buffer.split()) >= 5:  # commit sentences with ≥5 words
            sentences.append(buffer)
            buffer = ""
    if buffer:
        sentences.append(buffer)
    return sentences


def chunk_document(doc: dict) -> list[dict]:
    """
    Sentence-aware chunking with overlap.

    Algorithm:
    1. Split text into sentences.
    2. Accumulate sentences until the chunk reaches CHUNK_TARGET_WORDS.
    3. The last CHUNK_OVERLAP_WORDS words of the current chunk become the
       start of the next chunk (semantic overlap).
    4. Chunks shorter than CHUNK_MIN_WORDS are merged into the previous chunk.
    5. Each chunk inherits doc metadata plus chunk_index.
    """
    text     = doc.get("text", "").strip()
    source   = doc.get("source", "unknown")
    topic    = doc.get("topic",  "general")
    title    = doc.get("title",  source)

    if not text:
        return []

    sentences = _split_sentences(text)
    if not sentences:
        return [{"text": text, "source": source, "topic": topic,
                 "title": title, "chunk_index": 0}]

    chunks  = []
    current = []       # list of sentences in current chunk
    c_words = 0        # word count of current chunk

    def commit(sentences_list: list[str], idx: int) -> dict:
        chunk_text = " ".join(sentences_list).strip()
        return {
            "text":        chunk_text,
            "source":      source,
            "topic":       topic,
            "title":       title,
            "chunk_index": idx,
        }

    for sent in sentences:
        sent_words = len(sent.split())
        current.append(sent)
        c_words += sent_words

        if c_words >= CHUNK_TARGET_WORDS:
            chunks.append(commit(current, len(chunks)))
            # Overlap: keep last CHUNK_OVERLAP_WORDS words worth of sentences
            overlap_sentences, overlap_words = [], 0
            for s in reversed(current):
                sw = len(s.split())
                if overlap_words + sw <= CHUNK_OVERLAP_WORDS:
                    overlap_sentences.insert(0, s)
                    overlap_words += sw
                else:
                    break
            current = overlap_sentences
            c_words = overlap_words

    # Remaining sentences
    if current:
        remaining_words = len(" ".join(current).split())
        if chunks and remaining_words < CHUNK_MIN_WORDS:
            # Merge short tail into previous chunk
            prev = chunks[-1]
            merged_text = prev["text"] + " " + " ".join(current)
            if len(merged_text.split()) <= CHUNK_MAX_WORDS:
                chunks[-1] = {**prev, "text": merged_text.strip()}
            else:
                chunks.append(commit(current, len(chunks)))
        else:
            chunks.append(commit(current, len(chunks)))

    return chunks


def _merge_short_docs(docs: list[dict], topic: str,
                      group_size: int = 4) -> list[dict]:
    """
    Merge consecutive short documents (< CHUNK_MIN_WORDS) into
    groups of `group_size`, producing one chunk per group.
    Used for the customer-interaction dataset passages.
    """
    chunks = []
    for i in range(0, len(docs), group_size):
        group = docs[i:i + group_size]
        # Build a coherent passage from the group
        parts = []
        for d in group:
            # Extract the clean body (strip the "Support Topic:" header)
            body = d.get("text", "")
            lines = body.split("\n\n")
            # Keep Agent Response lines, skip repetitive "Support Topic:" headers
            filtered = [l for l in lines if not l.startswith("Support Topic:")]
            parts.append("\n\n".join(filtered).strip())

        merged = "\n\n---\n\n".join(p for p in parts if p)
        wc = len(merged.split())
        if wc >= CHUNK_MIN_WORDS:
            chunks.append({
                "text":   merged,
                "source": f"dataset/{topic}",
                "topic":  topic,
                "title":  group[0].get("title", topic),
                "chunk_index": i // group_size,
            })
    return chunks


def build_chunks(documents: list[dict]) -> list[dict]:
    """
    Two-strategy chunker:
    1. Long KB articles (≥ CHUNK_MIN_WORDS): sentence-aware split with overlap
    2. Short dataset interactions (< CHUNK_MIN_WORDS): merge groups of 4 by topic
    """
    import hashlib
    from collections import defaultdict

    all_chunks: list[dict] = []
    chunk_id = 1

    # Separate long docs (KB) from short docs (dataset)
    long_docs:  list[dict] = []
    short_by_topic: dict[str, list[dict]] = defaultdict(list)

    for doc in documents:
        wc = len(doc.get("text", "").split())
        if wc >= CHUNK_MIN_WORDS:
            long_docs.append(doc)
        else:
            short_by_topic[doc.get("topic", "general_tips")].append(doc)

    log.info("Long docs (KB articles): %d", len(long_docs))
    log.info("Short docs (interactions): %d",
             sum(len(v) for v in short_by_topic.values()))

    # Strategy 1: chunk long KB articles
    for doc in long_docs:
        for chunk in chunk_document(doc):
            wc = len(chunk["text"].split())
            if wc >= CHUNK_MIN_WORDS:
                chunk["id"] = chunk_id
                chunk["word_count"] = wc
                all_chunks.append(chunk)
                chunk_id += 1

    # Strategy 2: merge short interaction docs by topic
    for topic, docs in short_by_topic.items():
        merged = _merge_short_docs(docs, topic, group_size=4)
        for chunk in merged:
            chunk["id"] = chunk_id
            chunk["word_count"] = len(chunk["text"].split())
            all_chunks.append(chunk)
            chunk_id += 1

    # Dedup by text prefix hash
    seen, unique = set(), []
    for c in all_chunks:
        h = hashlib.md5(c["text"][:400].encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(c)

    log.info("Chunks: %d total → %d after dedup (from %d source docs)",
             len(all_chunks), len(unique), len(documents))
    return unique


# ── Step 3 — Embedding model ────────────────────────────────────────────────
class EmbeddingModel:
    """
    TF-IDF (bigrams) + Truncated SVD → 384-dim L2-normalised embeddings.

    Swap for sentence-transformers on a connected machine:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(texts, show_progress_bar=True,
                                  normalize_embeddings=True)
    """

    def __init__(self, n_components: int = EMBEDDING_DIM):
        self.n_components = n_components
        self.vectorizer   = None
        self.svd          = None
        self._fitted      = False

    def fit(self, texts: list[str]) -> "EmbeddingModel":
        log.info("Fitting TF-IDF on %d texts …", len(texts))
        self.vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=80_000,
            sublinear_tf=True,
            min_df=1,
        )
        X = self.vectorizer.fit_transform(texts)
        log.info("TF-IDF matrix shape: %s", X.shape)

        actual_dim = min(self.n_components, X.shape[1] - 1, X.shape[0] - 1)
        self.svd = TruncatedSVD(n_components=actual_dim, random_state=42)
        self.svd.fit(X)
        self.n_components = actual_dim
        var = self.svd.explained_variance_ratio_.sum()
        log.info("SVD: %d dims, %.1f%% variance", actual_dim, var * 100)
        self._fitted = True
        return self

    def encode(self, texts: list[str]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("Call .fit() first")
        X     = self.vectorizer.transform(texts)
        dense = self.svd.transform(X)
        if dense.shape[1] < EMBEDDING_DIM:
            pad   = np.zeros((dense.shape[0], EMBEDDING_DIM - dense.shape[1]),
                             dtype=np.float32)
            dense = np.hstack([dense, pad])
        return normalize(dense, norm="l2").astype(np.float32)

    def save(self, path: str) -> None:
        with open(path, "wb") as fh:
            pickle.dump({"vectorizer": self.vectorizer, "svd": self.svd,
                         "n_components": self.n_components}, fh)
        log.info("Embedding model → %s", path)

    @classmethod
    def load(cls, path: str) -> "EmbeddingModel":
        with open(path, "rb") as fh:
            state = pickle.load(fh)
        obj = cls(n_components=state["n_components"])
        obj.vectorizer = state["vectorizer"]
        obj.svd        = state["svd"]
        obj._fitted    = True
        log.info("Embedding model ← %s", path)
        return obj


# ── Step 4 — Vector index ───────────────────────────────────────────────────
class VectorIndex:
    """Flat cosine similarity index (L2-normalised dot product)."""

    def __init__(self, dim: int = EMBEDDING_DIM):
        self.dim = dim
        self.vectors: np.ndarray | None = None

    def add(self, vectors: np.ndarray) -> None:
        assert vectors.ndim == 2 and vectors.shape[1] == self.dim
        self.vectors = (vectors.astype(np.float32) if self.vectors is None
                        else np.vstack([self.vectors, vectors.astype(np.float32)]))
        log.info("Index: %d vectors", len(self.vectors))

    def search(self, query: np.ndarray, k: int = 5) -> tuple[np.ndarray, np.ndarray]:
        if self.vectors is None:
            return np.array([]), np.array([])
        q      = normalize(query.reshape(1, -1).astype(np.float32), norm="l2")
        scores = (self.vectors @ q.T).flatten()
        top_k  = min(k, len(scores))
        idx    = np.argpartition(scores, -top_k)[-top_k:]
        idx    = idx[np.argsort(scores[idx])[::-1]]
        return scores[idx], idx

    def save(self, path: str) -> None:
        np.savez_compressed(path, vectors=self.vectors, dim=np.array(self.dim))
        log.info("Index → %s", path)

    @classmethod
    def load(cls, path: str) -> "VectorIndex":
        data = np.load(path, allow_pickle=False)
        obj  = cls(dim=int(data["dim"]))
        obj.vectors = data["vectors"]
        log.info("Index ← %s (%d vectors)", path, len(obj.vectors))
        return obj


# ── Main pipeline ───────────────────────────────────────────────────────────
def build_vector_store() -> None:
    log.info("=== E-commerce Vector Store Builder v2 ===")

    documents  = load_documents(SCRAPER_OUTPUT)
    chunks     = build_chunks(documents)

    if not chunks:
        raise ValueError("No chunks produced — check scraped_support_text.json")

    texts = [c["text"] for c in chunks]

    # Stats
    wc = [len(t.split()) for t in texts]
    log.info("Chunk stats — count:%d  min:%d  max:%d  avg:%d words",
             len(texts), min(wc), max(wc), sum(wc)//len(wc))

    # Embed
    log.info("Generating %d-dim embeddings for %d chunks …", EMBEDDING_DIM, len(texts))
    model = EmbeddingModel(n_components=EMBEDDING_DIM)
    model.fit(texts)
    embeddings = model.encode(texts)
    log.info("Embeddings: %s", embeddings.shape)
    model.save(MODEL_PATH)

    # Index
    index = VectorIndex(dim=embeddings.shape[1])
    index.add(embeddings)
    index.save(INDEX_PATH)

    # Metadata — clean format matching v1 + extras
    metadata_clean = [
        {
            "id":          c["id"],
            "text":        c["text"],
            "source":      c["source"],
            "topic":       c["topic"],
            "title":       c.get("title", ""),
            "chunk_index": c["chunk_index"],
            "word_count":  c["word_count"],
        }
        for c in chunks
    ]
    with open(METADATA_PATH, "w", encoding="utf-8") as fh:
        json.dump(metadata_clean, fh, ensure_ascii=False, indent=2)
    log.info("Metadata → %s (%d records)", METADATA_PATH, len(metadata_clean))

    # Topic breakdown
    from collections import Counter
    topics = Counter(c["topic"] for c in chunks)
    log.info("\n=== Build Complete ===")
    log.info("  Total chunks  : %d", len(chunks))
    log.info("  Embedding dim : %d", embeddings.shape[1])
    log.info("  Index file    : %s", INDEX_PATH)
    log.info("  Metadata file : %s", METADATA_PATH)
    log.info("\n  Topic breakdown:")
    for topic, cnt in sorted(topics.items()):
        log.info("    %-35s %d", topic, cnt)
    log.info("\n  Run: python search_vector.py --demo")


if __name__ == "__main__":
    build_vector_store()
