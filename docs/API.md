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

## API Endpoints Overview

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/chat` | POST | Chat with AI assistant | API Key |
| `/api/files` | GET | List uploaded files | API Key |
| `/api/files/{filename}` | DELETE | Delete specific file | API Key |
| `/api/files` | DELETE | Delete all files | API Key |
| `/api/urls` | GET | List scraped URLs | API Key |
| `/api/urls/{filename}` | DELETE | Delete specific URL | API Key |
| `/api/urls` | DELETE | Delete all URLs | API Key |
| `/api/health` | GET | Health check | None |
| `/admin/upload-file` | POST | Upload document | API Key |
| `/admin/add-url` | POST | Add URL to scrape | API Key |
| `/admin/logs` | GET | View server logs | Admin |

---

## Chat Endpoint

### 🔹 POST `/api/chat`
**Chat with AI assistant using RAG + LoRA**

**Headers:**
- `X-API-Key`: Your API key

**Request Body:**
```json
{
  "query": "Who founded Wikipedia and what are its content policies?",
  "top_k": 3,
  "max_tokens": 200,
  "temperature": 0.3
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | required | Your question |
| `top_k` | int | 3 | Number of context chunks to retrieve |
| `max_tokens` | int | 200 | Maximum response length |
| `temperature` | float | 0.3 | Creativity (0.1 = focused, 1.0 = creative) |

**Response:**
```json
{
  "query": "Who founded Wikipedia?",
  "domain": "education",
  "company": "wikipedia",
  "sentiment": "neutral",
  "sentiment_confidence": 0.94,
  "response": "Wikipedia was founded by Jimmy Wales and Larry Sanger in January 2001...",
  "response_time_ms": 45000.5,
  "timestamp": "2026-03-29T10:30:00"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -d '{"query": "What is Wikipedia?", "top_k": 3}'
```

---

## File Management

### 🔹 GET `/api/files`
**List all uploaded files for your domain/company**

**Response:**
```json
{
  "success": true,
  "domain": "education",
  "company": "wikipedia",
  "files": [
    {
      "filename": "pdf_wikipedia_detailed.txt",
      "file_type": "raw",
      "size_bytes": 3043,
      "created_at": "2026-03-29T10:00:00"
    },
    {
      "filename": "wikipedia.pdf",
      "file_type": "original",
      "size_bytes": 15420,
      "created_at": "2026-03-29T09:55:00"
    }
  ],
  "total_count": 2
}
```

**Example:**
```bash
curl -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/files
```

---

### 🔹 DELETE `/api/files/{filename}`
**Delete a specific file and rebuild vector store**

**Response:**
```json
{
  "success": true,
  "message": "Deleted 2 file(s). Vector store will be rebuilt.",
  "domain": "education",
  "company": "wikipedia",
  "deleted_files": ["raw_data/pdf_old_doc.txt", "original_files/old_doc.pdf"],
  "vector_store_rebuilt": true
}
```

**Example:**
```bash
curl -X DELETE -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/files/old_doc.pdf
```

---

### 🔹 DELETE `/api/files`
**Delete ALL files for your domain/company**

⚠️ **Use with caution!** This deletes all files AND the vector store.

**Example:**
```bash
curl -X DELETE -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/files
```

---

## URL Management

### 🔹 GET `/api/urls`
**List all scraped URLs for your domain/company**

**Response:**
```json
{
  "success": true,
  "domain": "education",
  "company": "wikipedia",
  "urls": [
    {
      "filename": "url_wiki_Machine_learning.txt",
      "original_url": "Machine learning - Wikipedia",
      "size_bytes": 45000,
      "created_at": "2026-03-29T08:00:00"
    }
  ],
  "total_count": 1
}
```

**Example:**
```bash
curl -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/urls
```

---

### 🔹 DELETE `/api/urls/{filename}`
**Delete a specific URL file and rebuild vector store**

Use the filename from `/api/urls` listing (e.g., `url_wiki_Machine_learning.txt`).

**Response:**
```json
{
  "success": true,
  "message": "Deleted URL file 'url_wiki_Machine_learning.txt'. Vector store will be rebuilt.",
  "domain": "education",
  "company": "wikipedia",
  "deleted_url": "url_wiki_Machine_learning.txt",
  "vector_store_rebuilt": true
}
```

**Example:**
```bash
curl -X DELETE -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/urls/url_wiki_Machine_learning.txt
```

---

### 🔹 DELETE `/api/urls`
**Delete ALL URL files (keeps uploaded PDFs safe)**

**Example:**
```bash
curl -X DELETE -H "X-API-Key: sk_education_wikipedia_tes123" \
  http://localhost:8000/api/urls
```

---

## Content Upload

### 🔹 POST `/admin/upload-file`
**Upload PDF/DOCX/TXT document**

**Headers:**
- `X-API-Key`: Your API key (domain/company auto-detected)

**Form Data:**
- `file`: PDF/DOCX/TXT file

**Response:**
```json
{
  "success": true,
  "message": "File processed successfully",
  "domain": "education",
  "company": "wikipedia",
  "original_path": "original_files/education/wikipedia/refund.pdf",
  "extracted_path": "raw_data/education/wikipedia/pdf_refund.txt",
  "characters_extracted": 5420
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -F "file=@my_document.pdf"
```

**Supported formats:** PDF, DOCX, DOC, TXT

---

### 🔹 POST `/admin/add-url`
**Add URL to scrape**

**Request Body:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Wikipedia"
}
```

**Response:**
```json
{
  "success": true,
  "message": "URL fetched and processed successfully",
  "domain": "education",
  "company": "wikipedia",
  "url": "https://en.wikipedia.org/wiki/Wikipedia"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/admin/add-url \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -d '{"url": "https://en.wikipedia.org/wiki/Wikipedia"}'
```

---

## Health & Monitoring

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
  "timestamp": "2026-03-29T10:30:00"
}
```

---

### 🔹 GET `/admin/logs`
**View API logs** (Admin only)

**Query Parameters:**
- `lines`: Number of lines to return (default: 100)

**Example:**
```bash
curl http://localhost:8000/admin/logs?lines=50 \
  -H "X-API-Key: sk_admin_master_xyz999"
```

---

## Authentication

### Using Swagger UI (Recommended for Testing)

1. Open http://localhost:8000/docs
2. Click the **"Authorize"** button (🔓 lock icon)
3. Enter your API key (e.g., `sk_education_wikipedia_tes123`)
4. Click "Authorize" → "Close"
5. Now all endpoints will include your API key automatically

### API Key Types

| Type | Access | Example |
|------|--------|---------|
| **User Key** | Chat, Upload, URLs, File Management | `sk_education_wikipedia_tes123` |
| **Admin Key** | All above + Logs | `sk_admin_master_xyz999` |

### Data Isolation

Each API key only accesses its own domain/company data:
- `sk_education_wikipedia_*` → `data/*/education/wikipedia/`
- `sk_telecom_airtel_*` → `data/*/telecom/airtel/`

---

## Error Responses

| Code | Meaning | Example |
|------|---------|---------|
| 401 | Invalid/missing API key | `{"detail": "Invalid API key"}` |
| 403 | Admin access required | `{"detail": "Admin access required"}` |
| 404 | Resource not found | `{"detail": "Vector store not found..."}` |
| 500 | Server error | `{"detail": "Error generating response..."}` |

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER ACTIONS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Upload PDF ──────┐                                             │
│                    ▼                                             │
│              ┌──────────┐    ┌──────────────┐    ┌───────────┐  │
│   Add URL ───│ Raw Data │───▶│ Vector Store │───▶│    RAG    │  │
│              └──────────┘    └──────────────┘    │  + LoRA   │  │
│                    ▲               ▲             └─────┬─────┘  │
│                    │               │                   │        │
│   Delete File ─────┴── Rebuild ────┘                   ▼        │
│   Delete URL ──────────────────────────────────── Response      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Storage Structure

```
data/
├── raw_data/                    # Extracted text (used for vectors)
│   └── {domain}/
│       └── {company}/
│           ├── pdf_document.txt      # From PDF upload
│           └── url_webpage.txt       # From URL scrape
│
├── original_files/              # Original uploads (preserved)
│   └── {domain}/
│       └── {company}/
│           └── document.pdf
│
└── vector_stores/               # FAISS indexes
    └── {domain}/
        └── {company}/
            ├── vector.index     # FAISS index
            └── metadata.json    # Chunk metadata
```

---

## Best Practices

### For Better Responses

1. **Upload comprehensive documents** (500+ words each)
2. **Use `top_k=3` or higher** for complex questions
3. **Increase `max_tokens`** for detailed answers
4. **Keep related content together** in same domain/company

### For Data Management

1. **List before deleting**: Use `/api/files` or `/api/urls` first
2. **Delete specific files**: Avoid bulk delete when possible
3. **Check after delete**: Vector store rebuilds automatically

### For Production

1. **Use HTTPS** with reverse proxy (nginx/caddy)
2. **Add GPU** for faster inference (10-20x speedup)
3. **Implement caching** for frequent queries
4. **Monitor logs** regularly

---

## Troubleshooting

### Empty or Wrong Responses

| Problem | Cause | Solution |
|---------|-------|----------|
| Empty response | Token extraction issue | Server restart usually fixes |
| Wrong topic | Irrelevant files in vector store | Delete unwanted files via `/api/files/{filename}` |
| Partial answer | Low `top_k` or `max_tokens` | Increase parameters in request |

### Server Issues

| Problem | Solution |
|---------|----------|
| Port already in use | Kill existing: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess` |
| Slow startup | Normal - models loading (~30-60 sec) |
| Out of memory | Use smaller batch size or add swap |

---

## Interactive Documentation

Once server is running, visit:

- **Swagger UI**: http://localhost:8000/docs (Recommended)
- **ReDoc**: http://localhost:8000/redoc

Try out all endpoints directly in the browser!



