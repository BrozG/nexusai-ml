 # NexusAI ML Backend

Scalable AI-based customer support backend powered by LoRA fine-tuned Phi-2, RAG, and vector stores.

## Quick Start (FastAPI)

```bash
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Configure API keys
# Edit api_keys.json

# Start server
python run.py
```

Open docs: http://localhost:8000/docs

Health check:
```bash
curl http://localhost:8000/api/health
```

## API Keys

Keys are stored in [api_keys.json](api_keys.json). Each key maps to a domain and company.

Example:
```json
"sk_education_wikipedia_tes123": {
        "domain": "education",
        "company": "wikipedia",
        "role": "user",
        "description": "Wikipedia Education API Key"
}
```

Generate a new key:
```bash
python -c "import secrets; print('sk_' + secrets.token_urlsafe(32))"
```

## Core Endpoints

POST /api/chat
```bash
curl -X POST http://localhost:8000/api/chat \
        -H "Content-Type: application/json" \
        -H "X-API-Key: <your-key>" \
        -d '{"query":"What is Wikipedia?","top_k":3,"max_tokens":150,"temperature":0.3}'
```

POST /api/chat/compare (base vs adapter)
```bash
curl -X POST http://localhost:8000/api/chat/compare \
        -H "Content-Type: application/json" \
        -H "X-API-Key: <your-key>" \
        -d '{"query":"What is Wikipedia?","top_k":3,"max_tokens":150,"temperature":0.3}'
```

## Frontend Integration (BrozG/nexusai)

Frontend repo: https://github.com/BrozG/nexusai

### Run the UI

```bash
git clone https://github.com/BrozG/nexusai
cd nexusai
npm install

# Create .env.local
# FASTAPI_URL=http://localhost:8000

npm run dev
```

### Connect UI to this backend

The UI uses a Next.js API proxy at app/api/chat/route.ts. Update it to forward the `X-API-Key` header and send only the `query` (domain is inferred from the API key on the backend).

Example proxy handler:
```ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
        const { api_key, query, top_k, max_tokens, temperature } = await req.json()

        if (!api_key || !query) {
                return NextResponse.json({ error: 'Missing api_key or query' }, { status: 400 })
        }

        const res = await fetch(`${process.env.FASTAPI_URL}/api/chat`, {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': api_key,
                        'ngrok-skip-browser-warning': 'true'
                },
                body: JSON.stringify({ query, top_k, max_tokens, temperature })
        })

        const data = await res.json()
        return NextResponse.json({ response: data.response })
}
```

If you want domain switching in the UI, map each domain to its own API key and send the selected key from the client.

## Project Structure

```
nexsusai-ml/
├── src/                    # FastAPI + RAG pipeline
├── data/                   # Runtime data (raw, vector stores)
├── adapters/               # LoRA adapters
├── docs/                   # Documentation
├── logs/                   # Server logs
├── run.py                  # Server entrypoint
├── api_keys.json           # API key config
└── requirements.txt
```

## Docs

- [docs/QUICKSTART.md](docs/QUICKSTART.md)
- [docs/API.md](docs/API.md)

Extracts text from PDF, DOCX, and TXT files. Optionally saves original files.

```bash
# Show help
python src/ingest/pdf_handler.py --help

# Extract text only (saves to raw_data/)
python src/ingest/pdf_handler.py --file document.pdf --domain ecommerce --company amazon

# Save original + extract text (saves to policies/ AND raw_data/)
python src/ingest/pdf_handler.py --file document.pdf --domain ecommerce --company amazon --save-original

# List saved files
python src/ingest/pdf_handler.py --list --domain ecommerce --company amazon
```

**Python API (for WebUI):**
```python
from src.ingest.pdf_handler import handle_pdf, handle_pdf_with_original

# Extract text only
result = handle_pdf(file_bytes, "ecommerce", "amazon", "policy.pdf")
# -> raw_data/ecommerce/amazon/pdf_policy.txt

# Save original + extract text
result = handle_pdf_with_original(file_bytes, "ecommerce", "amazon", "policy.pdf")
# -> policies/ecommerce/amazon/policy.pdf
# -> raw_data/ecommerce/amazon/pdf_policy.txt
```

**Output Structure:**
```
policies/                      # Original files (--save-original)
└── ecommerce/amazon/policy.pdf

raw_data/                      # Extracted text
└── ecommerce/amazon/pdf_policy.txt
```

---

### 3. Vector Builder (FAISS Index)

Builds searchable vector stores from extracted text.

```bash
# Show help
python src/vector/vector_builder.py --help

# Build vector store for specific domain/company
python src/vector/vector_builder.py --build --domain education --company mit

# Build all vector stores
python src/vector/vector_builder.py --build-all

# Watch mode (auto-rebuild on file changes)
python src/vector/vector_builder.py --watch

# Rebuild specific vector store
python src/vector/vector_builder.py --rebuild --domain ecommerce --company amazon

# Get vector store statistics
python src/vector/vector_builder.py --stats
```

**Output Structure:**
```
vector_stores/
└── education/
    └── mit/
        ├── vector.index       # FAISS index file
        └── metadata.json      # Chunk metadata and sources
```

---

### 4. Simple RAG (Search & Generation)

Simplified RAG without domain classifier - you specify domain/company directly.

```bash
# Show help
python src/rag/simple_rag.py --help

# Search only (no generation)
python src/rag/simple_rag.py --search "refund policy" --domain ecommerce --company amazon

# Search with more results
python src/rag/simple_rag.py --search "grades" --domain education --company mit --top-k 5

# Full RAG (search + generate with Phi-2 + LoRA)
python src/rag/simple_rag.py --generate "How do I get a refund?" --domain ecommerce --company amazon

# Interactive mode
python src/rag/simple_rag.py --interactive --domain telecom --company airtel
```

**Search Output Example:**
```
Query: "refund policy"
Domain: ecommerce/amazon

Results:
1. [Relevance: 0.89] Source: pdf_refund_policy.txt
   "Returns are accepted within 30 days of purchase..."

2. [Relevance: 0.76] Source: url_help_center.txt
   "To request a refund, go to Your Orders..."
```

---

## Complete Workflow Example

```bash
# Step 1: Fetch data from web
python src/fetcher/universal_fetcher.py --url "https://mit.edu/admissions" --domain education --company mit

# Step 2: Process PDF documents
python src/ingest/pdf_handler.py --file handbook.pdf --domain education --company mit

# Step 3: Build vector store
python src/vector/vector_builder.py --build --domain education --company mit

# Step 4: Search the knowledge base
python src/rag/simple_rag.py --search "admission requirements" --domain education --company mit

# Optional: Start watch mode for auto-updates
python src/vector/vector_builder.py --watch
```

---

## Three-Tier Storage Architecture

```
policies/           ->    raw_data/           ->    vector_stores/
(Original Files)          (Extracted Text)          (FAISS Index)
     |                         |                         |
     v                         v                         v
  Untouched              Chunked text              Embeddings
  PDF/DOCX               for processing            for search
```

| Tier | Purpose | Contents |
|------|---------|----------|
| `policies/` | Original file archive | Untouched uploaded PDFs |
| `raw_data/` | Text extraction | Extracted text from URLs/PDFs |
| `vector_stores/` | Search index | FAISS vectors + metadata |

---

## Training Results

### LoRA Adapter Training Analysis

![LoRA Training Analysis](assets/lora_training_analysis_clean.png)

| Domain | Samples | Start Loss | End Loss | Reduction |
|---|---|---|---|---|
| E-commerce | 1,000 | 3.14 | 1.24 | **60.4%** |
| Education | 1,000 | 2.97 | 1.20 | **59.6%** |
| Telecom | 1,500 | 1.98 | 0.35 | **82.8%** |

---

### Base Phi-2 vs LoRA Fine-tuned - Quality Comparison

![Base vs LoRA Comparison](assets/base_vs_lora_comparison_graph.png)

| Domain | Base Phi-2 Score | LoRA Score | Improvement |
|---|---|---|---|
| E-commerce | 2.4 / 5 | 4.6 / 5 | **+92%** |
| Education | 1.8 / 5 | 4.2 / 5 | **+133%** |
| Telecom | 1.4 / 5 | 5.0 / 5 | **+257%** |

---

### Domain Classifier Analysis

![Domain Classifier Analysis](assets/domain_classifier_analysis.png)

| Domain | Precision | Recall | F1-Score |
|---|---|---|---|
| E-commerce | 1.00 | 1.00 | 1.00 |
| Education | 1.00 | 1.00 | 1.00 |
| Telecom | 1.00 | 1.00 | 1.00 |

---

## Tech Stack

| Component | Technology |
|---|---|
| Base LLM | Microsoft Phi-2 |
| Fine-tuning Method | LoRA (Low-Rank Adaptation) |
| Vector Store | FAISS (Facebook AI Similarity Search) |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Web Scraping | BeautifulSoup4, Requests |
| Document Processing | PyPDF2, python-docx |
| Scheduling | APScheduler |
| File Monitoring | Watchdog |
| Training | Python, PyTorch, HuggingFace |

---

## Related

- [NexusAI Web UI](https://github.com/BrozG/nexusai) - Next.js frontend built by [@kuhitjeetaray](https://github.com/kuhitjeetaray)
- [Live Demo](https://nexusai-beryl.vercel.app)

---

## Author

**BrozG** - AI Architecture, LoRA Pipeline, Domain Classifier, Vector Store, Training

[![GitHub](https://img.shields.io/badge/GitHub-BrozG-blue)](https://github.com/BrozG)

---

## License

MIT

Copyright (c) 2026 BrozG



