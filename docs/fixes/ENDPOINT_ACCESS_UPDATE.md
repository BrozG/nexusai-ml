# 🔓 API Endpoint Access Update

## Change Summary

**Date**: 2026-03-27
**Change**: Opened file upload and URL scraping endpoints to all valid API key holders

---

## What Changed

### Before
- `/admin/upload-file` - **Admin only**
- `/admin/add-url` - **Admin only**
- Regular users could only query via `/api/chat`
- Could not upload their own documents or URLs

### After
- `/admin/upload-file` - **Any valid API key** ✅
- `/admin/add-url` - **Any valid API key** ✅
- Each business can upload files and URLs for their own domain/company
- Domain/company automatically determined from API key

---

## Technical Changes

### src/server/main.py

**Upload File Endpoint:**
```python
# BEFORE
@app.post("/admin/upload-file")
async def upload_file(
    key_info: Dict = Depends(validate_admin_key)  # ❌ Admin only
):
    domain = key_info.get("domain", "ecommerce")  # ❌ Fallback defaults
    company = key_info.get("company", "default")

# AFTER
@app.post("/admin/upload-file")
async def upload_file(
    key_info: Dict = Depends(validate_api_key)  # ✅ Any valid key
):
    domain = key_info["domain"]  # ✅ From API key
    company = key_info["company"]  # ✅ From API key
```

**Add URL Endpoint:**
```python
# BEFORE
@app.post("/admin/add-url")
async def add_url(
    key_info: Dict = Depends(validate_admin_key)  # ❌ Admin only
):
    domain = key_info.get("domain", "ecommerce")  # ❌ Fallback defaults
    company = key_info.get("company", "default")

# AFTER
@app.post("/admin/add-url")
async def add_url(
    key_info: Dict = Depends(validate_api_key)  # ✅ Any valid key
):
    domain = key_info["domain"]  # ✅ From API key
    company = key_info["company"]  # ✅ From API key
```

---

## Security Implications

### ✅ What's Secure

1. **Automatic isolation**: Each API key can only upload to their own domain/company
2. **No cross-contamination**: Amazon can't upload to MIT's folder
3. **API key required**: Still requires valid authentication
4. **Domain/company enforced**: Extracted from API key, not user input

### 🔒 Data Isolation Example

```
API Key: sk_ecommerce_amazon_abc123
├─ domain: "ecommerce"
├─ company: "amazon"
└─ Can only upload to:
    ├─ policies/ecommerce/amazon/
    ├─ raw_data/ecommerce/amazon/
    └─ vector_stores/ecommerce/amazon/

API Key: sk_education_mit_def456
├─ domain: "education"
├─ company: "mit"
└─ Can only upload to:
    ├─ policies/education/mit/
    ├─ raw_data/education/mit/
    └─ vector_stores/education/mit/
```

**No way to upload to another company's directory!**

---

## Usage Examples

### Upload File (Business Client)

**Before** (not allowed):
```bash
# Would get 403 Forbidden
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_ecommerce_amazon_abc123" \
  -F "file=@refund_policy.pdf"
```

**After** (allowed):
```bash
# Now works! Uploads to ecommerce/amazon automatically
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_ecommerce_amazon_abc123" \
  -F "file=@refund_policy.pdf"

# Response:
{
  "success": true,
  "domain": "ecommerce",   # From API key
  "company": "amazon",      # From API key
  "original_path": "policies/ecommerce/amazon/refund_policy.pdf",
  "extracted_path": "raw_data/ecommerce/amazon/pdf_refund_policy.txt"
}
```

### Add URL (Business Client)

**Before** (not allowed):
```bash
# Would get 403 Forbidden
curl -X POST http://localhost:8000/admin/add-url \
  -H "X-API-Key: sk_education_mit_def456" \
  -d '{"url": "https://mit.edu/admissions"}'
```

**After** (allowed):
```bash
# Now works! Scrapes to education/mit automatically
curl -X POST http://localhost:8000/admin/add-url \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_mit_def456" \
  -d '{"url": "https://mit.edu/admissions"}'

# Response:
{
  "success": true,
  "domain": "education",   # From API key
  "company": "mit",         # From API key
  "url": "https://mit.edu/admissions"
}
```

---

## Admin vs User Permissions

### Standard API Key
**Can access:**
- ✅ `POST /api/chat` - Chat with AI
- ✅ `POST /admin/upload-file` - Upload own files
- ✅ `POST /admin/add-url` - Add own URLs
- ✅ `GET /api/health` - Health check

**Cannot access:**
- ❌ `GET /admin/logs` - View server logs (admin only)

### Admin API Key
**Can access:**
- ✅ All endpoints above
- ✅ `GET /admin/logs` - View server logs

---

## Benefits of This Change

### 1. Self-Service
Businesses can manage their own knowledge base without admin intervention:
- Upload new product manuals
- Add FAQ URLs
- Update policy documents
- Refresh training materials

### 2. Faster Onboarding
New clients can:
1. Get API key
2. Upload documents immediately
3. Start using AI chat
4. No waiting for admin to upload files

### 3. Better UX
- Businesses control their own data
- Immediate updates (auto vector rebuild)
- No bottleneck on admin

### 4. Scalability
- Admin doesn't need to manage every upload
- Hundreds of clients can upload simultaneously
- Each isolated to their own directory

---

## Testing

### Test with User Key
```bash
# Upload file
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: sk_ecommerce_amazon_abc123" \
  -F "file=@test.pdf"

# Add URL
curl -X POST http://localhost:8000/admin/add-url \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_ecommerce_amazon_abc123" \
  -d '{"url": "https://example.com"}'
```

Both should return `200 OK` with domain/company matching the API key.

### Test Isolation
```bash
# Try to upload to different company (NOT POSSIBLE)
# The domain/company is extracted from YOUR API key
# No way to specify a different company in the request
```

---

## Migration Notes

### For Existing Users
**No changes required!**
- Existing admin keys still work
- Existing user keys now have additional permissions
- No API breaking changes

### For New Integrations
Update your client code:
```python
# Upload file with regular API key (no admin needed)
import requests

headers = {
    "X-API-Key": "sk_ecommerce_amazon_abc123"  # Regular key works now!
}

files = {
    "file": open("document.pdf", "rb")
}

response = requests.post(
    "http://localhost:8000/admin/upload-file",
    headers=headers,
    files=files
)

# Domain/company automatically set from API key
print(response.json())
```

---

## Documentation Updated

Files updated to reflect this change:
- ✅ `src/server/main.py` - Endpoint validation changed
- ✅ `README_API.md` - API documentation updated
- ✅ `test_api.py` - Test script updated
- ✅ This document - Change summary

---

## Rollback Plan

If needed, revert by changing:
```python
Depends(validate_api_key)  # Current
# back to
Depends(validate_admin_key)  # Original
```

---

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Upload access** | Admin only | Any API key ✅ |
| **URL access** | Admin only | Any API key ✅ |
| **Domain/company** | Fallback defaults | From API key ✅ |
| **Security** | Centralized | Isolated per key ✅ |
| **User experience** | Admin bottleneck | Self-service ✅ |
| **Scalability** | Limited | High ✅ |

**Result**: Businesses can now self-manage their AI knowledge base while maintaining complete data isolation! 🎉



