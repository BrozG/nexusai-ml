# 🧪 Complete Testing Guide

## Quick Start Testing

### Step 1: Start the Server
```bash
python run.py
```

**Expected output:**
```
============================================================
NexusAI API Server Starting...
============================================================
Step 1/5: Loading API keys...
Loaded 4 API keys
Step 2/5: Loading sentiment model...
✓ Sentiment model loaded successfully
Step 3/5: Initializing RAG system...
✓ RAG system ready with 3 adapters
Step 4/5: Initializing components...
✓ Universal fetcher initialized
Step 5/5: Starting vector builder watch mode...
✓ Vector builder watch mode thread started
============================================================
✓ Server startup complete!
============================================================
```

---

## Automated Testing

### Run Full Test Suite
```bash
python tests/test_api.py
```

**Tests:**
- ✅ Health endpoint
- ✅ Invalid API key rejection
- ✅ Admin logs access
- ✅ File upload
- ✅ Chat endpoint

---

## Manual Testing (Step-by-Step)

### 1️⃣ Test Health Check (No Auth)

```bash
curl http://localhost:8000/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "uptime_seconds": 45.2,
  "loaded_adapters": ["ecommerce", "education", "telecom"],
  "sentiment_model_loaded": true,
  "vector_builder_active": true,
  "timestamp": "2026-03-27T12:00:00"
}
```

---

### 2️⃣ Test File Upload (Wikipedia Education)

Create a test file:
```bash
echo "Wikipedia is a free online encyclopedia. Students can access millions of articles for research and learning." > test_wikipedia.txt
```

Upload it:
```bash
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -F "file=@test_wikipedia.txt"
```

**Expected response:**
```json
{
  "success": true,
  "message": "File processed successfully",
  "domain": "education",
  "company": "wikipedia",
  "original_path": "data/policies/education/wikipedia/test_wikipedia.txt",
  "extracted_path": "data/raw_data/education/wikipedia/pdf_test_wikipedia.txt",
  "characters_extracted": 120
}
```

**Verify files created:**
```bash
# Check original file
dir data\policies\education\wikipedia\test_wikipedia.txt

# Check extracted text
dir data\raw_data\education\wikipedia\pdf_test_wikipedia.txt

# Wait 30 seconds for vector store to build, then check
dir data\vector_stores\education\wikipedia\vector.index
dir data\vector_stores\education\wikipedia\metadata.json
```

---

### 3️⃣ Test URL Addition (MIT Education)

```bash
curl -X POST http://localhost:8000/admin/add-url \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_mit_def456" \
  -d "{\"url\": \"https://example.com\"}"
```

**Expected response:**
```json
{
  "success": true,
  "message": "URL fetched and processed successfully",
  "domain": "education",
  "company": "mit",
  "url": "https://example.com"
}
```

**Verify files created:**
```bash
# Check scraped content
dir data\raw_data\education\mit\url_*.txt

# Wait 30 seconds for vector store to build, then check
dir data\vector_stores\education\mit\vector.index
```

---

### 4️⃣ Test Chat with RAG (After Uploading Docs)

**First, ensure you have documents uploaded (do step 2 first)**

Then test chat:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -d "{\"query\": \"What is Wikipedia?\"}"
```

**Expected response:**
```json
{
  "query": "What is Wikipedia?",
  "domain": "education",
  "company": "wikipedia",
  "sentiment": "neutral",
  "sentiment_confidence": 0.92,
  "response": "Based on the available information, Wikipedia is...",
  "response_time_ms": 1250.5,
  "timestamp": "2026-03-27T12:00:00"
}
```

---

### 5️⃣ Test Different Companies (Data Isolation)

**Upload to Airtel (Telecom):**
```bash
echo "Airtel provides 4G and 5G mobile services across India." > test_airtel.txt

curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_telecom_airtel_ghi789" \
  -F "file=@test_airtel.txt"
```

**Verify isolation:**
```bash
# Airtel's file should be in telecom/airtel
dir data\raw_data\telecom\airtel\pdf_test_airtel.txt

# NOT in education/wikipedia
dir data\raw_data\education\wikipedia\pdf_test_airtel.txt
# (Should not exist)
```

---

### 6️⃣ Test Admin Logs Access

**With admin key (should work):**
```bash
curl http://localhost:8000/admin/logs?lines=10 \
  -H "X-API-Key: sk_admin_master_xyz999"
```

**Expected response:**
```json
{
  "lines": [
    "2026-03-27 12:00:00 - INFO - Server started",
    "2026-03-27 12:01:00 - INFO - Chat request received",
    ...
  ],
  "count": 10,
  "total_lines": 250
}
```

**With user key (should fail):**
```bash
curl http://localhost:8000/admin/logs?lines=10 \
  -H "X-API-Key: sk_education_wikipedia_tes123"
```

**Expected response:**
```json
{
  "detail": "Admin access required"
}
```

---

### 7️⃣ Test Invalid API Key

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: invalid-key-12345" \
  -d "{\"query\": \"Test\"}"
```

**Expected response:**
```json
{
  "detail": "Invalid API key"
}
```

---

## Interactive Testing with Swagger UI

### Access API Docs
Open in browser:
```
http://localhost:8000/docs
```

**Features:**
- 🔍 See all endpoints
- 📝 View request/response schemas
- 🧪 Test endpoints directly in browser
- 🔑 Enter API key once, test all endpoints

**How to use:**
1. Click **"Authorize"** button (top right)
2. Enter API key: `sk_education_wikipedia_tes123`
3. Click each endpoint to expand
4. Click **"Try it out"**
5. Fill in parameters
6. Click **"Execute"**
7. See response

---

## Testing Checklist

### ✅ Basic Functionality
- [ ] Server starts without errors
- [ ] Health endpoint returns 200
- [ ] All 3 LoRA adapters loaded
- [ ] Sentiment model loaded
- [ ] Vector builder active

### ✅ Authentication
- [ ] Valid API key accepted
- [ ] Invalid API key rejected (401)
- [ ] User key cannot access admin logs (403)
- [ ] Admin key can access all endpoints

### ✅ File Upload
- [ ] File uploads successfully
- [ ] Original saved to `data/policies/`
- [ ] Text extracted to `data/raw_data/`
- [ ] Vector store builds (wait 30s)
- [ ] Domain/company match API key

### ✅ URL Scraping
- [ ] URL fetches successfully
- [ ] Content saved to `data/raw_data/`
- [ ] Vector store builds (wait 30s)
- [ ] Domain/company match API key

### ✅ Chat with RAG
- [ ] Chat returns response
- [ ] Sentiment detected
- [ ] Response time logged
- [ ] Uses correct domain/company
- [ ] 404 if no vector store exists

### ✅ Data Isolation
- [ ] Each company has separate directories
- [ ] Cannot upload to another company's folder
- [ ] Vector stores kept separate

---

## Performance Testing

### Response Time Test
```bash
# Time the chat request
time curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -d "{\"query\": \"Test query\"}"
```

**Expected:**
- First request: 10-30 seconds (model loading)
- Subsequent: <2 seconds

### Concurrent Requests Test
```bash
# Run multiple requests simultaneously
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -H "X-API-Key: sk_education_wikipedia_tes123" \
    -d "{\"query\": \"Test $i\"}" &
done
wait
```

---

## Troubleshooting Tests

### If Health Check Fails
```bash
# Check server logs
tail -50 logs/api.log

# Verify server is running
curl http://localhost:8000/
```

### If Chat Returns 404
```bash
# Check if vector store exists
dir data\vector_stores\education\wikipedia\vector.index

# If not, upload a document first (step 2)
# Then wait 30 seconds for rebuild
```

### If Upload Fails
```bash
# Check file size
dir test_file.txt

# Check API key is valid
curl http://localhost:8000/api/health

# Check logs for errors
Get-Content -Tail 20 logs\api.log
```

### If Vector Store Not Building
```bash
# Check vector builder is active
curl http://localhost:8000/api/health
# Should show: "vector_builder_active": true

# Check raw_data exists
dir data\raw_data\education\wikipedia\

# Wait longer (vector building takes 10-30 seconds)

# Check vector builder log
type vector_builder.log
```

---

## Windows PowerShell Testing

If using PowerShell instead of bash:

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/api/health"

# Upload file
$file = Get-Item "test.txt"
$form = @{
    file = $file
}
Invoke-RestMethod -Uri "http://localhost:8000/admin/upload-file" `
    -Method Post `
    -Headers @{"X-API-Key" = "sk_education_wikipedia_tes123"} `
    -Form $form

# Chat
$body = @{
    query = "What is Wikipedia?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "X-API-Key" = "sk_education_wikipedia_tes123"
    } `
    -Body $body
```

---

## Complete Test Workflow

### End-to-End Test (5 minutes)

```bash
# 1. Start server
python run.py
# Wait for startup to complete

# 2. In new terminal: Health check
curl http://localhost:8000/api/health

# 3. Create test file
echo "Test content for Wikipedia" > test.txt

# 4. Upload file
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -F "file=@test.txt"

# 5. Wait for vector store to build
timeout /t 30

# 6. Verify vector store exists
dir data\vector_stores\education\wikipedia\vector.index

# 7. Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -d "{\"query\": \"Tell me about the content\"}"

# 8. Check logs
curl http://localhost:8000/admin/logs?lines=20 \
  -H "X-API-Key: sk_admin_master_xyz999"
```

---

## Success Criteria

✅ **All tests pass when:**
1. Server starts without crashes
2. Health shows all systems active
3. Files upload to correct directories
4. Vector stores auto-build
5. Chat returns responses with sentiment
6. Data isolation verified
7. Admin access works
8. User access restricted appropriately

---

## Quick Test Commands

**Copy-paste ready commands:**

```bash
# Health
curl http://localhost:8000/api/health

# Upload (create test.txt first)
curl -X POST http://localhost:8000/admin/upload-file -H "X-API-Key: sk_education_wikipedia_tes123" -F "file=@test.txt"

# Chat (after upload + 30s wait)
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -H "X-API-Key: sk_education_wikipedia_tes123" -d "{\"query\":\"test\"}"

# Admin logs
curl http://localhost:8000/admin/logs?lines=10 -H "X-API-Key: sk_admin_master_xyz999"
```

---

**Your NexusAI API is ready for comprehensive testing!** 🚀



