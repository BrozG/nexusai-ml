# 🚀 NexusAI API Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- 8GB+ RAM (16GB recommended for running all models)
- CUDA-capable GPU (optional but recommended)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First run may take 10-30 minutes to download models (~3-4GB total):
- Phi-2 base model (~2.7GB)
- Sentence transformer (~200MB)
- Sentiment model (~500MB)
- LoRA adapters (included in repo as .zip files)

### 2. Configure API Keys

Edit `api_keys.json` in the project root:

```json
{
  "api_keys": {
    "sk_education_wikipedia_tes123": {
      "domain": "education",
      "company": "wikipedia",
      "role": "user",
      "description": "Wikipedia Education API Key"
    },
    "sk_admin_master_xyz999": {
      "domain": "admin",
      "company": "admin",
      "role": "admin",
      "description": "Admin Master Key - Full Access"
    }
  },
  "admin_keys": [
    "sk_admin_master_xyz999"
  ]
}
```

**⚠️ IMPORTANT**: Replace these example keys with your own random keys in production!

Generate secure keys:
```bash
python -c "import secrets; print('sk_' + secrets.token_urlsafe(32))"
```

### 3. Prepare Data (Optional but Recommended)

Before starting the server, you can pre-populate vector stores:

#### Option A: Upload documents via CLI

```bash
# Process a PDF (from project root)
python src/pdf_handler.py --file my_policy.pdf --domain ecommerce --company amazon --save-original

# Scrape a URL
python src/universal_fetcher.py --domain ecommerce --company amazon --input https://example.com/faq

# Build vector stores
python src/vector_builder.py --build
```

#### Option B: Upload via API after server starts

See "First Use" section below.

### 4. Start the Server

```bash
python run.py
```

With custom settings:
```bash
python run.py --host 0.0.0.0 --port 8000 --reload
```

**Startup will take 30-60 seconds** as models load. You should see:

```
============================================================
NexusAI API Server Starting...
============================================================
Loaded 4 API keys
Loaded 1 admin keys
Loading sentiment model: cardiffnlp/twitter-roberta-base-sentiment-latest
✓ Sentiment model loaded successfully
Initializing RAG system...
Loading Phi-2 base model...
Loading ecommerce adapter...
✓ ecommerce adapter loaded
Loading education adapter...
✓ education adapter loaded
Loading telecom adapter...
✓ telecom adapter loaded
✓ RAG system ready with 3 adapters
Starting vector builder in watch mode...
✓ Vector builder watch mode started
============================================================
✓ Server startup complete!
============================================================
```

Server is now running at: **http://localhost:8000**

## First Use

### Step 1: Check Health

```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "uptime_seconds": 45.2,
  "loaded_adapters": ["ecommerce", "education", "telecom"],
  "sentiment_model_loaded": true,
  "vector_builder_active": true
}
```

### Step 2: Upload Your First Document

```bash
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -F "file=@my_document.pdf"
```

Or use the interactive docs at: **http://localhost:8000/docs**
(Click "Authorize" and enter your API key first)

### Step 3: Make Your First Chat Request

Wait 30 seconds for vector store to build, then:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -d '{
    "query": "What is your refund policy?",
    "top_k": 3
  }'
```

### Step 4: Manage Your Files

List uploaded files:
```bash
curl -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/files
```

Delete unwanted files (auto-rebuilds vector store):
```bash
curl -X DELETE -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/files/old_document.pdf
```

### Step 5: Manage Scraped URLs

List scraped URLs:
```bash
curl -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/urls
```

Delete URL content:
```bash
curl -X DELETE -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/urls/url_example_page.txt
```

## Testing

Run the automated test suite:

```bash
python tests/test_api.py
```

This will test:
- ✅ Health endpoint
- ✅ API key validation
- ✅ Admin endpoints
- ✅ File upload
- ✅ Chat endpoint

## Interactive API Documentation

Once server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly in the browser!

## Directory Structure

```
nexsusai-ml/
├── run.py                 # ← Server launcher
├── api_keys.json          # ← API key configuration
├── requirements.txt
│
├── src/                   # Source code
│   ├── main.py           # FastAPI server
│   ├── simple_rag.py     # RAG pipeline
│   ├── pdf_handler.py    # Document processing
│   ├── universal_fetcher.py
│   └── vector_builder.py
│
├── data/                  # Runtime data
│   ├── original_files/   # Original uploaded files (preserved)
│   ├── raw_data/         # Extracted text (used for vectors)
│   └── vector_stores/    # FAISS indexes
│
├── tests/                 # Test files
│   └── test_api.py
│
├── docs/                  # Documentation
│   ├── API.md            # Endpoint reference
│   ├── QUICKSTART.md     # This file
│   └── fixes/            # Troubleshooting guides
│
├── logs/                  # Server logs
└── adapters/             # LoRA adapters (.zip files)
```

## Common Issues

### 🔴 "RAG system not initialized"

**Cause**: Models failed to load

**Solution**:
1. Check `logs/api.log` for errors
2. Ensure you have enough RAM (8GB minimum)
3. Try restarting the server
4. Models download on first run - check internet connection

### 🔴 "Vector store not found for domain/company"

**Cause**: No documents uploaded yet for that domain/company

**Solution**:
1. Upload documents via `/admin/upload-file`
2. Wait 30 seconds for vector store to build
3. Or manually build: `python src/vector_builder.py --build --domain ecommerce --company amazon`

### 🔴 "Invalid API key"

**Cause**: Wrong key or missing X-API-Key header

**Solution**:
1. Check `api_keys.json` for valid keys
2. Ensure header is `X-API-Key` (case-sensitive)
3. Copy key exactly (no extra spaces)

### 🔴 Server is slow on first request

**Expected behavior**: First request loads models into memory (10-30s)

**Subsequent requests are fast** (<2s with GPU, 30-120s on CPU)

### 🔴 Wrong topic in response

**Cause**: Irrelevant files in vector store polluting results

**Solution**:
1. List your files: `GET /api/files`
2. Delete unwanted files: `DELETE /api/files/{filename}`
3. Vector store rebuilds automatically
4. See `docs/fixes/RAG_RESPONSE_FIXES.md` for details

### 🔴 Empty or partial responses

**Cause**: Token extraction or prompt format issues

**Solution**:
1. Use `top_k=3` or higher for complex questions
2. Increase `max_tokens` in request (default: 200)
3. Check server version - fixes applied in March 2026
4. See `docs/fixes/RAG_RESPONSE_FIXES.md` for details

## Production Deployment

### Using Gunicorn (Recommended)

```bash
gunicorn src.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### Environment Variables

Create `.env` file (see `.env.example`):

```env
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

## Security Checklist

- [ ] Replace example API keys with random secure keys
- [ ] Add `api_keys.json` to `.gitignore` (already done)
- [ ] Restrict CORS origins in production
- [ ] Use HTTPS (configure reverse proxy like nginx)
- [ ] Monitor `logs/api.log` for suspicious activity

---

**Server running at: http://localhost:8000**

**API Docs: http://localhost:8000/docs**

🎉 **You're all set!**
