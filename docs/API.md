# NexusAI API Documentation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit `api_keys.json` (in project root) to add your API keys:
```json
{
  "api_keys": {
    "your-api-key-here": {
      "domain": "ecommerce",
      "company": "amazon",
      "role": "user"
    }
  },
  "admin_keys": ["your-admin-key-here"]
}
```

### 3. Start Server
```bash
python run.py
```

Or with custom settings:
```bash
python run.py --host 0.0.0.0 --port 8000 --reload
```

Server will start on: `http://localhost:8000`

---

## API Endpoints

### 🔹 POST `/api/chat`
**Chat with AI assistant**

**Headers:**
- `X-API-Key`: Your API key

**Request Body:**
```json
{
  "query": "How do I get a refund?",
  "top_k": 3,
  "max_tokens": 150,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "query": "How do I get a refund?",
  "domain": "ecommerce",
  "company": "amazon",
  "sentiment": "neutral",
  "sentiment_confidence": 0.92,
  "response": "Based on our refund policy...",
  "response_time_ms": 1250.5,
  "timestamp": "2026-03-27T10:30:00"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_ecommerce_amazon_abc123" \
  -d '{"query": "How do I return an item?"}'
```

---

### 🔹 POST `/admin/upload-file`
**Upload PDF/DOCX/TXT document** (Any valid API key)

**Headers:**
- `X-API-Key`: Your API key (domain/company auto-detected)

**Form Data:**
- `file`: PDF/DOCX/TXT file

**Response:**
```json
{
  "success": true,
  "message": "File processed successfully",
  "domain": "ecommerce",
  "company": "amazon",
  "original_path": "policies/ecommerce/amazon/refund.pdf",
  "extracted_path": "raw_data/ecommerce/amazon/pdf_refund.txt",
  "characters_extracted": 5420
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_ecommerce_amazon_abc123" \
  -F "file=@refund_policy.pdf"
```

**Note:** Files are uploaded to your company's directory based on your API key.

---

### 🔹 POST `/admin/add-url`
**Add URL to scrape** (Any valid API key)

**Headers:**
- `X-API-Key`: Your API key (domain/company auto-detected)

**Request Body:**
```json
{
  "url": "https://example.com/help/refunds"
}
```

**Response:**
```json
{
  "success": true,
  "message": "URL fetched and processed successfully",
  "domain": "ecommerce",
  "company": "amazon",
  "url": "https://example.com/help/refunds"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/admin/add-url \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_ecommerce_amazon_abc123" \
  -d '{"url": "https://example.com/help"}'
```

**Note:** URLs are fetched and stored in your company's directory based on your API key.

---

### 🔹 GET `/api/health`
**Check API health** (No auth required)

**Response:**
```json
{
  "status": "healthy",
  "uptime_seconds": 3600.5,
  "loaded_adapters": ["ecommerce", "education", "telecom"],
  "sentiment_model_loaded": true,
  "vector_builder_active": true,
  "timestamp": "2026-03-27T10:30:00"
}
```

**Example:**
```bash
curl http://localhost:8000/api/health
```

---

### 🔹 GET `/admin/logs`
**View API logs** (Admin only)

**Headers:**
- `X-API-Key`: Admin API key

**Query Parameters:**
- `lines`: Number of lines to return (default: 100)

**Response:**
```json
{
  "lines": [
    "2026-03-27 10:30:00 - INFO - Chat request received",
    "2026-03-27 10:30:01 - INFO - Response generated"
  ],
  "count": 100,
  "total_lines": 5420
}
```

**Example:**
```bash
curl http://localhost:8000/admin/logs?lines=50 \
  -H "X-API-Key: sk_admin_master_xyz999"
```

---

## Authentication

All endpoints (except `/api/health`) require an API key in the `X-API-Key` header.

### Standard API Keys
- **Access to**:
  - `/api/chat` - Chat with AI
  - `/admin/upload-file` - Upload documents to your company
  - `/admin/add-url` - Add URLs to scrape for your company
- **Domain/company**: Automatically determined by key configuration
- **Permissions**: Can only manage data for their own domain/company

### Admin API Keys
- **Access to**: All endpoints including:
  - `/admin/logs` - View server logs
- **Permissions**: Full system access
- **Listed in**: `admin_keys` array in `api_keys.json`

**Note:** Upload and URL endpoints are no longer admin-only. Any valid API key holder can upload files and URLs for their own company.

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid API key"
}
```

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found
```json
{
  "detail": "Vector store not found for ecommerce/amazon. Please upload documents first."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error generating response: ..."
}
```

---

## Startup Behavior

When the server starts, it automatically:

1. ✅ Loads `api_keys.json` for authentication
2. ✅ Loads Phi-2 base model
3. ✅ Pre-loads all 3 LoRA adapters (ecommerce, education, telecom)
4. ✅ Loads sentiment model (cardiffnlp/twitter-roberta-base-sentiment-latest)
5. ✅ Starts vector builder in watch mode (auto-rebuilds on file changes)

**Startup logs:**
```
============================================================
NexusAI API Server Starting...
============================================================
Loaded 4 API keys
Loaded 1 admin keys
Loading sentiment model: cardiffnlp/twitter-roberta-base-sentiment-latest
✓ Sentiment model loaded successfully
Initializing RAG system...
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
✓ Loaded adapters: ['ecommerce', 'education', 'telecom']
✓ Sentiment model: Active
✓ Vector builder: Active
============================================================
```

---

## Background Tasks

### Vector Builder Watch Mode
- Monitors `data/raw_data/` directory for changes
- Automatically rebuilds vector stores when files are added/modified
- Runs in background thread
- Debounces to avoid duplicate rebuilds (5-second cooldown)

### Async Rebuilds
- File uploads and URL fetches trigger vector store rebuilds
- Runs in background (doesn't block API response)
- Logs progress to `logs/api.log`

---

## Logging

All requests are logged to `logs/api.log` with:
- Timestamp
- Domain/company
- Query (truncated)
- Sentiment detected
- Response time
- Success/failure status

**Example log entry:**
```
2026-03-27 10:30:00 - INFO - Chat request - Domain: ecommerce, Company: amazon, Query: How do I return an item?
2026-03-27 10:30:00 - INFO - Sentiment: neutral (confidence: 0.920)
2026-03-27 10:30:01 - INFO - Response generated in 1250.52ms - Sentiment: neutral
```

---

## Production Deployment

### Using Uvicorn directly:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn (recommended):
```bash
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

---

## Security Best Practices

1. **Use strong API keys** (32+ random characters)
2. **Keep `api_keys.json` out of version control** (add to `.gitignore`)
3. **Use HTTPS in production** (configure reverse proxy)
4. **Rotate admin keys regularly**
5. **Configure CORS properly** (restrict `allow_origins` in production)
6. **Monitor `logs/api.log` for suspicious activity**

---

## Troubleshooting

### Server won't start
- Check `api_keys.json` exists and is valid JSON
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check ports aren't already in use

### Chat endpoint returns 404
- Vector store doesn't exist for domain/company
- Upload documents via `/admin/upload-file` first
- Or run `python src/vector_builder.py --build` manually

### Slow responses
- First request loads models (can take 10-30 seconds)
- Subsequent requests are fast (models cached)
- Consider using GPU for faster inference

### Sentiment always "neutral"
- Sentiment model may not have downloaded
- Check `logs/api.log` for errors
- Model downloads on first use (~500MB)

---

## Interactive API Documentation

Once server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try out endpoints directly in the browser!
