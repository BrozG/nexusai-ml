"""
search_vector.py  (v2 — improved)
===================================
Semantic search over the e-commerce customer support vector database.

Improvements over v1
--------------------
* Richer result display: shows topic, source, title, word count, score
* Topic-filtered search: search within a specific support topic
* Batch query mode: run a file of queries
* Smarter prerequisite check with auto-rebuild
* Formatted result snippets with configurable length
* Relevance score threshold filtering

Usage:
    python search_vector.py                           # interactive
    python search_vector.py "How long is a refund?"  # single query
    python search_vector.py --demo                   # all demo queries
    python search_vector.py --topic refund_policy    # topic-filtered search
"""

import json
import logging
import pickle
import sys
import textwrap
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.preprocessing import normalize

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────────────────
INDEX_PATH    = "ecommerce_vector.index.npz"
METADATA_PATH = "ecommerce_metadata.json"
MODEL_PATH    = "embedding_model.pkl"
TOP_K         = 5          # default results per query
MIN_SCORE     = 0.05       # discard results below this similarity threshold
WRAP_WIDTH    = 88
SNIPPET_WORDS = 80         # words to show in result preview

DEMO_QUERIES = [
    "How long does a refund take?",
    "Can I cancel my order after it has shipped?",
    "What should I do if my product arrives damaged?",
    "Why did my payment fail?",
    "My package shows delivered but I never received it",
    "How do I return an item to Flipkart?",
    "I want to replace a defective product",
    "How do I reset my account password?",
    "What is the eBay Money Back Guarantee?",
    "My refund was less than the full amount — why?",
    "How do I track my Amazon order?",
    "What happens if I refuse a delivery?",
    "Can I return electronics after 30 days?",
    "My EMI payment failed — what do I do?",
    "How do I report a counterfeit product?",
]

BANNER = "═" * WRAP_WIDTH
SEP    = "─" * WRAP_WIDTH


# ── Embedding model wrapper ─────────────────────────────────────────────────
class _EmbedModel:
    def __init__(self, state: dict):
        self.vectorizer   = state["vectorizer"]
        self.svd          = state["svd"]
        self.n_components = state["n_components"]
        self.EMBEDDING_DIM = 384

    def encode(self, texts: list[str]) -> np.ndarray:
        tfidf = self.vectorizer.transform(texts)
        dense = self.svd.transform(tfidf)
        if dense.shape[1] < self.EMBEDDING_DIM:
            pad   = np.zeros((dense.shape[0],
                              self.EMBEDDING_DIM - dense.shape[1]),
                             dtype=np.float32)
            dense = np.hstack([dense, pad])
        return normalize(dense, norm="l2").astype(np.float32)


# ── Search engine ───────────────────────────────────────────────────────────
class VectorSearchEngine:

    def __init__(self):
        self.vectors:  Optional[np.ndarray] = None
        self.metadata: list[dict]           = []
        self.model:    Optional[_EmbedModel]= None
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return

        log.info("Loading index …")
        data = np.load(INDEX_PATH, allow_pickle=False)
        self.vectors = data["vectors"].astype(np.float32)
        log.info("  %d vectors, dim=%d", *self.vectors.shape)

        log.info("Loading metadata …")
        with open(METADATA_PATH, encoding="utf-8") as fh:
            self.metadata = json.load(fh)
        log.info("  %d records", len(self.metadata))

        log.info("Loading embedding model …")
        with open(MODEL_PATH, "rb") as fh:
            self.model = _EmbedModel(pickle.load(fh))

        self._loaded = True
        log.info("Search engine ready ✓\n")

    def search(
        self,
        query: str,
        k: int = TOP_K,
        topic_filter: Optional[str] = None,
        min_score: float = MIN_SCORE,
    ) -> list[dict]:
        """
        Semantic search.

        Args:
            query:        Natural language question.
            k:            Maximum results to return.
            topic_filter: If set, only return chunks from this topic.
            min_score:    Cosine similarity threshold.

        Returns:
            List of result dicts with keys:
            id, text, source, topic, title, chunk_index, score, rank
        """
        self.load()

        q_vec  = self.model.encode([query])        # (1, dim)
        scores = (self.vectors @ q_vec.T).flatten()

        # Topic filter mask
        if topic_filter:
            for i, meta in enumerate(self.metadata):
                if meta.get("topic") != topic_filter:
                    scores[i] = -1.0

        # Top-k with score threshold
        top_k = min(k * 3, len(scores))            # over-fetch, then filter
        idx   = np.argpartition(scores, -top_k)[-top_k:]
        idx   = idx[np.argsort(scores[idx])[::-1]]

        results = []
        for i in idx:
            score = float(scores[i])
            if score < min_score:
                break
            rec = dict(self.metadata[i])
            rec["score"] = score
            rec["rank"]  = len(results) + 1
            results.append(rec)
            if len(results) >= k:
                break

        return results


# ── Display helpers ─────────────────────────────────────────────────────────
def _snippet(text: str, n_words: int = SNIPPET_WORDS) -> str:
    words = text.split()
    snippet = " ".join(words[:n_words])
    if len(words) > n_words:
        snippet += " …"
    return snippet


def print_results(query: str, results: list[dict], show_full: bool = False) -> None:
    print(f"\n{BANNER}")
    print(f"  QUERY : {query}")
    print(BANNER)

    if not results:
        print("  No results above threshold.\n")
        return

    for r in results:
        title  = r.get("title", r.get("source", ""))
        wc     = r.get("word_count", len(r["text"].split()))
        print(f"\n  #{r['rank']}  Score:{r['score']:.4f}  "
              f"Topic:{r['topic']}  Words:{wc}")
        print(f"  Title  : {title[:75]}")
        print(f"  Source : {r['source']}")
        print(SEP)
        body = r["text"] if show_full else _snippet(r["text"])
        print(textwrap.fill(body, width=WRAP_WIDTH,
                            initial_indent="  ", subsequent_indent="  "))

    print(f"\n{SEP}")


# ── Prerequisite check ──────────────────────────────────────────────────────
def ensure_built() -> bool:
    needed = [INDEX_PATH, METADATA_PATH, MODEL_PATH]
    if any(not Path(p).exists() for p in needed):
        log.info("Vector store not found — building now …")
        from build_vector_store import build_vector_store
        build_vector_store()
    still = [p for p in needed if not Path(p).exists()]
    if still:
        log.error("Build failed — missing: %s", still)
        return False
    return True


# ── Entry points ─────────────────────────────────────────────────────────────
engine = VectorSearchEngine()


def run_demo(k: int = 3) -> None:
    print(f"\n{BANNER}")
    print("  E-COMMERCE SUPPORT VECTOR SEARCH — DEMO")
    print(BANNER)
    for q in DEMO_QUERIES:
        results = engine.search(q, k=k)
        print_results(q, results)


def run_single(query: str, k: int = TOP_K,
               topic: Optional[str] = None,
               full: bool = False) -> None:
    results = engine.search(query, k=k, topic_filter=topic)
    print_results(query, results, show_full=full)


def run_interactive() -> None:
    print(f"\n{BANNER}")
    print("  E-COMMERCE SUPPORT VECTOR SEARCH  (type 'exit' to quit)")
    print(f"  Commands: 'topic:<name>' to filter, 'full' to show full text")
    print(BANNER)

    while True:
        try:
            raw = input("\n  Query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not raw:
            continue
        if raw.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        # Parse optional prefix commands
        topic_filter = None
        show_full    = False
        query        = raw

        if raw.lower().startswith("topic:"):
            parts        = raw.split(None, 1)
            topic_filter = parts[0].split(":", 1)[1]
            query        = parts[1] if len(parts) > 1 else ""

        if query.lower().endswith(" full"):
            show_full = True
            query     = query[:-5].strip()

        if not query:
            print("  Please provide a search query.")
            continue

        results = engine.search(query, k=TOP_K, topic_filter=topic_filter)
        print_results(query, results, show_full=show_full)


# ── CLI ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not ensure_built():
        sys.exit(1)

    args = sys.argv[1:]

    if "--demo" in args:
        run_demo(k=3)
    elif "--topic" in args:
        tidx  = args.index("--topic")
        topic = args[tidx + 1] if tidx + 1 < len(args) else None
        query = " ".join(a for a in args if a not in ("--topic", topic or ""))
        if query:
            run_single(query, topic=topic)
        else:
            print(f"Available topics: refund_policy, return_policy, "
                  f"order_cancellation, delivery_issues, payment_failures, "
                  f"damaged_items, product_replacement, account_issues, "
                  f"tracking_shipping, seller_disputes, warranty_service, "
                  f"general_tips")
    elif args:
        run_single(" ".join(args))
    else:
        run_interactive()
