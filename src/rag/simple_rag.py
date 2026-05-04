"""
Simplified RAG Pipeline (No Domain Classifier Needed)
User specifies domain directly → searches that folder → generates with LoRA
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List

# Set UTF-8 for Windows (only when running standalone)
if sys.platform == "win32" and __name__ == "__main__":
    try:
        import io
        if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except Exception:
        pass

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
    print("Install: pip install torch transformers peft sentence-transformers faiss-cpu")


class SimpleRAG:
    """
    Simple RAG without domain classification.
    User specifies domain/company → we use that vector store + LoRA adapter.
    """

    def __init__(self, base_dir: str = None):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Required dependencies not installed")

        # Default to project root (two levels above src/ subpackages)
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parents[2]
        else:
            self.base_dir = Path(base_dir)

        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Loading Phi-2 base model...")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Fix padding

        # Determine device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Load model - use simple device placement for PEFT compatibility
        # device_map="auto" with offloading causes meta tensor issues with PEFT
        self.base_model = AutoModelForCausalLM.from_pretrained(
            "microsoft/phi-2",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        # Move to device
        if device == "cuda":
            self.base_model = self.base_model.to(device)

        # Caches
        self.lora_adapters = {}
        self.vector_stores = {}

        # Debug toggle for adapter usage logs
        self.debug_adapters = os.getenv("NEXUSAI_DEBUG_ADAPTERS", "0").lower() in ("1", "true", "yes")

        print("✓ SimpleRAG initialized!\n")

    def _load_vector_store(self, domain: str, company: str) -> Dict:
        """Load vector store from folder structure."""
        key = f"{domain}/{company}"

        if key in self.vector_stores:
            return self.vector_stores[key]

        # Paths based on your folder structure (now in data/ directory)
        index_path = self.base_dir / "data" / "vector_stores" / domain / company / "vector.index"
        metadata_path = self.base_dir / "data" / "vector_stores" / domain / company / "metadata.json"

        if not index_path.exists():
            available = list((self.base_dir / "data" / "vector_stores").rglob("vector.index"))
            raise FileNotFoundError(
                f"Vector store not found: {index_path}\n"
                f"Available stores: {[str(p.parent.relative_to(self.base_dir / 'data' / 'vector_stores')) for p in available]}"
            )

        # Load FAISS index
        index = faiss.read_index(str(index_path))

        # Load metadata
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        store = {"index": index, "metadata": metadata}
        self.vector_stores[key] = store

        print(f"✓ Loaded vector store: {domain}/{company} ({len(metadata['chunks'])} chunks)")
        return store

    def search(self, query: str, domain: str, company: str, top_k: int = 3) -> List[Dict]:
        """
        Search for relevant context chunks.

        Args:
            query: User question
            domain: Domain folder name (e.g., 'education', 'ecommerce')
            company: Company folder name (e.g., 'mit', 'amazon')
            top_k: Number of chunks to retrieve

        Returns:
            List of dicts with text, source, distance, relevance
        """
        store = self._load_vector_store(domain, company)

        # Encode query to vector
        query_vector = self.embedding_model.encode([query])

        # Search FAISS index
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

        return results

    def _load_lora_adapter(self, domain: str):
        """Load LoRA adapter for domain."""
        if domain in self.lora_adapters:
            if self.debug_adapters:
                print(f"DEBUG - Reusing cached LoRA adapter: {domain}")
            return self.lora_adapters[domain]

        adapter_path = self.base_dir / "adapters" / f"{domain}_adapter"

        # Unzip if needed
        if not adapter_path.exists():
            zip_path = self.base_dir / "adapters" / f"{domain}_adapter.zip"
            if zip_path.exists():
                import zipfile
                print(f"Extracting {domain} adapter...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(adapter_path)
            else:
                raise FileNotFoundError(f"Adapter not found: {zip_path}")

        print(f"Loading {domain} LoRA adapter...")
        
        # Load PEFT adapter
        model = PeftModel.from_pretrained(
            self.base_model, 
            str(adapter_path)
        )

        self.lora_adapters[domain] = model
        if self.debug_adapters:
            print(f"DEBUG - LoRA adapter active for domain: {domain}")
        return model

    def _clean_answer(self, text: str) -> str:
        """Strip prompt echoes and leading punctuation from model output."""
        if not text:
            return ""

        cleaned = text.strip()

        if "Answer:" in cleaned:
            cleaned = cleaned.split("Answer:")[-1].strip()

        for prefix in ("Context information:", "Based on the context above", "Question:"):
            if cleaned.startswith(prefix):
                cleaned = "\n".join(cleaned.splitlines()[1:]).strip()

        cleaned = cleaned.lstrip(" ,;:.-\n\t")
        return cleaned

    def _get_model_device(self, model):
        """Best-effort device lookup for model tensors."""
        if hasattr(model, "device"):
            return model.device
        return next(model.parameters()).device

    def _generate_with_model(self, model, inputs, max_new_tokens: int, temperature: float) -> str:
        """Generate and clean answer for a given model using prepared inputs."""
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )

        input_length = inputs['input_ids'].shape[1]
        generated_tokens = outputs[0][input_length:]

        full_response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        generated_text = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        answer = self._clean_answer(generated_text)
        if len(answer) < 20:
            answer = self._clean_answer(full_response)

        return answer

    def generate(
        self,
        query: str,
        domain: str,
        company: str,
        top_k: int = 3,
        max_new_tokens: int = 150,
        temperature: float = 0.7,
        include_base: bool = False
    ) -> Dict:
        """
        Complete RAG: Search → Generate

        Args:
            query: User question
            domain: Domain folder name
            company: Company folder name
            top_k: Number of context chunks
            max_new_tokens: Max tokens to generate
            temperature: Sampling temperature

        Returns:
            Dict with query, context_chunks, context, and generated answer
        """
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print(f"Domain: {domain}")
        print(f"Company: {company}")
        print(f"{'='*70}\n")

        # Step 1: Search for context
        print("Step 1: Searching for relevant context...")
        context_chunks = self.search(query, domain, company, top_k)

        # Build context string
        context = "\n\n".join([
            f"[Source: {chunk['source']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])

        print(f"✓ Found {len(context_chunks)} relevant chunks\n")

        # Step 2: Load LoRA adapter
        print("Step 2: Loading LoRA adapter...")
        model = self._load_lora_adapter(domain)
        print("✓ Adapter loaded\n")
        if self.debug_adapters:
            print(f"DEBUG - Adapter applied for request: domain={domain}, company={company}")

        # Step 3: Generate response
        print("Step 3: Generating response...")

        # Build prompt with context trimmed to keep the Answer marker in-window
        max_input_tokens = 1024
        prefix = "Context information:\n"
        suffix = (
            "\n\nBased on the context above, answer the following question:\n"
            f"Question: {query}\n"
            "Answer:"
        )

        base_tokens = self.tokenizer.encode(prefix + suffix, add_special_tokens=False)
        available = max_input_tokens - len(base_tokens)
        if available < 0:
            available = 0

        context_tokens = self.tokenizer.encode(context, add_special_tokens=False)
        if len(context_tokens) > available:
            context_tokens = context_tokens[:available]

        trimmed_context = self.tokenizer.decode(
            context_tokens,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        prompt = f"{prefix}{trimmed_context}{suffix}"

        print(f"DEBUG - Prompt length: {len(prompt)} chars")
        print(f"DEBUG - Context chunks found: {len(context_chunks)}")
        print(f"DEBUG - First context chunk: {context_chunks[0] if context_chunks else 'NONE'}")

        # Tokenize (prompt already trimmed to max_input_tokens)
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=False)
        adapter_device = self._get_model_device(model)
        inputs_adapter = {k: v.to(adapter_device) for k, v in inputs.items()}
        
        print(f"DEBUG - Input token count: {inputs['input_ids'].shape[1]}")

        # Generate (adapter)
        answer = self._generate_with_model(
            model,
            inputs_adapter,
            max_new_tokens=max_new_tokens,
            temperature=temperature
        )

        base_answer = None
        if include_base:
            print("Step 4: Generating base model response...")
            base_device = self._get_model_device(self.base_model)
            inputs_base = {k: v.to(base_device) for k, v in inputs.items()}
            base_answer = self._generate_with_model(
                self.base_model,
                inputs_base,
                max_new_tokens=max_new_tokens,
                temperature=temperature
            )
        
        print(f"DEBUG - Generated answer: {answer[:200]}")
        if base_answer is not None:
            print(f"DEBUG - Base model answer: {base_answer[:200]}")

        print(f"DEBUG - Final answer length: {len(answer)} chars")

        print("✓ Generated!\n")
        print(f"{'='*70}")
        print(f"Answer: {answer}")
        print(f"{'='*70}\n")

        return {
            "query": query,
            "domain": domain,
            "company": company,
            "context_chunks": context_chunks,
            "context": context,
            "answer": answer,
            "base_answer": base_answer
        }


# Demo usage
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║              Simple RAG Pipeline - No Classifier             ║
    ╚══════════════════════════════════════════════════════════════╝

    NO domain classification needed!
    You specify domain/company directly from folder structure.

    Folder structure:
        vector_stores/
        ├── education/
        │   └── mit/
        ├── ecommerce/
        │   └── amazon/
        └── telecom/
            └── airtel/

    You just say: domain='education', company='mit'
    Pipeline uses those folders automatically!
    """)

    # Check if dependencies are available
    if not DEPENDENCIES_AVAILABLE:
        print("\n⚠️  This is a reference implementation.")
        print("Install dependencies to run:")
        print("  pip install torch transformers peft sentence-transformers faiss-cpu")
        sys.exit(0)

    # Initialize
    print("\nInitializing RAG pipeline...")
    rag = SimpleRAG()

    # Example 1: Search only (like your current search_test.py)
    print("\n" + "="*70)
    print("EXAMPLE 1: Search Only")
    print("="*70)

    results = rag.search(
        query="What is MIT OpenCourseWare?",
        domain="education",
        company="mit",
        top_k=2
    )

    print("\nSearch Results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Relevance: {result['relevance']:.4f}")
        print(f"   Source: {result['source']}")
        print(f"   Text: {result['text'][:200]}...")

    # Example 2: Full RAG with generation
    print("\n\n" + "="*70)
    print("EXAMPLE 2: Full RAG (Search + Generate)")
    print("="*70)

    try:
        result = rag.generate(
            query="What courses does MIT offer for free?",
            domain="education",
            company="mit",
            top_k=3
        )

        print("\n📊 Result Summary:")
        print(f"  Context chunks used: {len(result['context_chunks'])}")
        print(f"  Generated answer length: {len(result['answer'])} chars")

    except Exception as e:
        print(f"\n⚠️  Generation failed: {e}")
        print("This is expected if Phi-2 model isn't downloaded yet.")

