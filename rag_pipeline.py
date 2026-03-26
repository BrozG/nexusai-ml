"""
Complete RAG Pipeline with Phi-2 + LoRA
Integrates vector search with domain-specific LoRA adapters
"""

import json
import pickle
import sys
from pathlib import Path
from typing import Dict, List

# Set UTF-8 for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import faiss
    import torch
    from sentence_transformers import SentenceTransformer
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    print(f"Missing dependency: {e}")
    print("This is a reference implementation showing how to integrate.")


class NexusAI:
    """Complete RAG pipeline with domain classification and LoRA adapters."""

    def __init__(self, base_dir: str = "."):
        if not DEPENDENCIES_AVAILABLE:
            print("Dependencies not loaded. This is a demo/reference only.")
            return

        self.base_dir = Path(base_dir)

        # Load domain classifier
        print("Loading domain classifier...")
        with open(self.base_dir / "domain_classifier.pkl", "rb") as f:
            self.domain_classifier = pickle.load(f)

        # Load embedding model for vector search
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load base Phi-2 model
        print("Loading Phi-2 base model...")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
        self.base_model = AutoModelForCausalLM.from_pretrained(
            "microsoft/phi-2",
            torch_dtype=torch.float32,
            device_map="auto",
            trust_remote_code=True
        )

        # Cache for loaded LoRA adapters
        self.lora_adapters = {}

        # Cache for loaded vector stores
        self.vector_stores = {}

        print("✓ NexusAI initialized successfully!")

    def _get_domain(self, query: str) -> str:
        """Classify the domain of the query."""
        domain = self.domain_classifier.predict([query])[0]
        print(f"  Domain: {domain}")
        return domain

    def _load_vector_store(self, domain: str, company: str) -> Dict:
        """Load vector store for a specific company."""
        key = f"{domain}/{company}"

        if key in self.vector_stores:
            return self.vector_stores[key]

        index_path = self.base_dir / "vector_stores" / domain / company / "vector.index"
        metadata_path = self.base_dir / "vector_stores" / domain / company / "metadata.json"

        if not index_path.exists():
            raise FileNotFoundError(f"Vector store not found: {index_path}")

        # Load FAISS index
        index = faiss.read_index(str(index_path))

        # Load metadata
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        store = {
            "index": index,
            "metadata": metadata
        }

        self.vector_stores[key] = store
        return store

    def _search_vectors(self, query: str, domain: str, company: str, top_k: int = 3) -> List[Dict]:
        """Search vector store for relevant context."""
        print(f"  Searching vector store: {domain}/{company}")

        # Load vector store
        store = self._load_vector_store(domain, company)

        # Encode query
        query_vector = self.embedding_model.encode([query])

        # Search
        distances, indices = store["index"].search(query_vector.astype('float32'), top_k)

        # Get chunks
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(store["metadata"]["chunks"]):
                chunk = store["metadata"]["chunks"][idx]
                results.append({
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "distance": float(distances[0][i]),
                    "relevance": 1 / (1 + distances[0][i])
                })

        print(f"  Found {len(results)} relevant chunks")
        return results

    def _load_lora_adapter(self, domain: str):
        """Load LoRA adapter for specific domain."""
        if domain in self.lora_adapters:
            return self.lora_adapters[domain]

        adapter_path = self.base_dir / "adapters" / f"{domain}_adapter"

        # Unzip if needed
        if not adapter_path.exists():
            zip_path = self.base_dir / "adapters" / f"{domain}_adapter.zip"
            if zip_path.exists():
                import zipfile
                print(f"  Extracting {domain} adapter...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(adapter_path)

        print(f"  Loading {domain} LoRA adapter...")
        model = PeftModel.from_pretrained(self.base_model, str(adapter_path))

        self.lora_adapters[domain] = model
        return model

    def _generate_response(
        self,
        query: str,
        context: str,
        domain: str,
        max_length: int = 200,
        temperature: float = 0.7
    ) -> str:
        """Generate response using Phi-2 + LoRA adapter."""
        # Load appropriate LoRA adapter
        model = self._load_lora_adapter(domain)

        # Build prompt with context (RAG pattern)
        prompt = f"""Context: {context}

User: {query}
Assistant:"""

        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt").to(model.device)

        # Generate with LoRA-adapted model
        print(f"  Generating response with {domain} adapter...")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the assistant's response
        if "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()

        return response

    def answer(
        self,
        query: str,
        company: str,
        top_k: int = 3,
        max_length: int = 200
    ) -> Dict:
        """
        Complete RAG pipeline: Classify → Search → Generate

        Args:
            query: User question
            company: Which company's data to search
            top_k: Number of context chunks to retrieve
            max_length: Max tokens in generated response

        Returns:
            Dict with domain, context chunks, and generated answer
        """
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print(f"Company: {company}")
        print(f"{'='*70}\n")

        # Step 1: Classify domain
        print("Step 1: Domain Classification")
        domain = self._get_domain(query)

        # Step 2: Vector search for context
        print("\nStep 2: Vector Search")
        context_chunks = self._search_vectors(query, domain, company, top_k)

        # Combine context
        context = "\n\n".join([chunk["text"] for chunk in context_chunks])

        # Step 3: Generate response with LoRA
        print("\nStep 3: Generate Response")
        answer = self._generate_response(query, context, domain, max_length)

        print(f"\n{'='*70}")
        print("✓ Complete!")
        print(f"{'='*70}\n")

        return {
            "query": query,
            "domain": domain,
            "company": company,
            "context_chunks": context_chunks,
            "context": context,
            "answer": answer
        }


# Simple search-only version (no LLM generation)
class SimpleRetriever:
    """Just vector search without LLM generation."""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_stores = {}

    def _load_vector_store(self, domain: str, company: str) -> Dict:
        """Load vector store."""
        key = f"{domain}/{company}"

        if key in self.vector_stores:
            return self.vector_stores[key]

        index_path = self.base_dir / "vector_stores" / domain / company / "vector.index"
        metadata_path = self.base_dir / "vector_stores" / domain / company / "metadata.json"

        if not index_path.exists():
            raise FileNotFoundError(f"Vector store not found: {index_path}")

        index = faiss.read_index(str(index_path))

        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        store = {"index": index, "metadata": metadata}
        self.vector_stores[key] = store
        return store

    def search(self, query: str, domain: str, company: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant chunks (NO generation)."""
        store = self._load_vector_store(domain, company)
        query_vector = self.embedding_model.encode([query])
        distances, indices = store["index"].search(query_vector.astype('float32'), top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(store["metadata"]["chunks"]):
                chunk = store["metadata"]["chunks"][idx]
                results.append({
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "distance": float(distances[0][i]),
                    "relevance": 1 / (1 + distances[0][i])
                })

        return results


# Example usage
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           NexusAI RAG Pipeline - Integration Example        ║
    ╚══════════════════════════════════════════════════════════════╝

    This shows how to integrate:
    1. Domain Classification (domain_classifier.pkl)
    2. Vector Search (FAISS + sentence-transformers)
    3. LoRA Generation (Phi-2 + domain adapters)

    CURRENT: Using SimpleRetriever (search only, no generation)
    NEXT: Use NexusAI class when you want full RAG with Phi-2
    """)

    # Demo with search-only (what you're using now)
    print("\n" + "="*70)
    print("DEMO: Search-Only Mode (Current)")
    print("="*70 + "\n")

    retriever = SimpleRetriever()
    results = retriever.search(
        query="What is MIT OpenCourseWare?",
        domain="education",
        company="mit",
        top_k=3
    )

    print(f"Found {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. Relevance: {result['relevance']:.4f}")
        print(f"   Text: {result['text'][:150]}...")
        print()

    print("\n" + "="*70)
    print("NEXT: Full RAG Pipeline (with Phi-2 + LoRA)")
    print("="*70 + "\n")

    print("""
    When you're ready to add generation:

    ```python
    # Initialize full pipeline
    ai = NexusAI()

    # Get answer with context
    result = ai.answer(
        query="How do I return a product?",
        company="amazon"
    )

    print(f"Domain: {result['domain']}")
    print(f"Answer: {result['answer']}")
    ```

    This will:
    1. Classify domain → "ecommerce"
    2. Search vectors → Get relevant chunks
    3. Load ecommerce_adapter.zip
    4. Generate answer with Phi-2 + LoRA using context
    """)
