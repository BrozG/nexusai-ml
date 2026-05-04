# ✅ NexusAI Setup Checklist

Use this checklist to ensure your NexusAI server is properly configured and running.

## 📋 Pre-Deployment Checklist

### 1. Dependencies
- [ ] Python 3.8+ installed
- [ ] All requirements installed: `pip install -r requirements.txt`
- [ ] 8GB+ RAM available
- [ ] ~10GB disk space for models

### 2. Configuration Files
- [ ] `api_keys.json` created with secure keys
- [ ] Admin keys configured in `admin_keys` array
- [ ] User keys configured with correct domain/company mappings
- [ ] `.gitignore` includes `api_keys.json` and `.env`
- [ ] API keys are strong (32+ random characters)

### 3. Directory Structure
- [ ] `logs/` directory created (auto-created on first run)
- [ ] `adapters/` contains `.zip` files or extracted folders
- [ ] `data/raw_data/` exists (will be created if missing)
- [ ] `data/vector_stores/` exists (will be created if missing)
- [ ] `data/policies/` exists (will be created if missing)

### 4. Initial Data (Optional)
- [ ] Sample documents uploaded
- [ ] Vector stores built for at least one domain/company
- [ ] Test with: `python src/vector/vector_builder.py --build`

---

## 🚀 First Startup Checklist

### 1. Start Server
```bash
python run.py
```

- [ ] Server starts without errors
- [ ] No import errors
- [ ] API keys loaded successfully
- [ ] Models begin downloading (if first run)

### 2. Wait for Startup (30-60 seconds)
Monitor console output for:
- [ ] ✓ API keys loaded
- [ ] ✓ Sentiment model loaded
- [ ] ✓ RAG system initialized
- [ ] ✓ Phi-2 base model loaded
- [ ] ✓ ecommerce adapter loaded
- [ ] ✓ education adapter loaded
- [ ] ✓ telecom adapter loaded
- [ ] ✓ Vector builder started
- [ ] ✓ Server startup complete

### 3. Verify Health
```bash
curl http://localhost:8000/api/health
```

Check response:
- [ ] `status: "healthy"`
- [ ] `loaded_adapters: ["ecommerce", "education", "telecom"]`
- [ ] `sentiment_model_loaded: true`
- [ ] `vector_builder_active: true`

---

## 🧪 Testing Checklist

### 1. API Documentation
- [ ] Visit http://localhost:8000/docs
- [ ] Swagger UI loads correctly
- [ ] All 5 endpoints visible
- [ ] Schemas display properly

### 2. Authentication Tests
```bash
# Should return 401
curl -X POST http://localhost:8000/api/chat \
  -H "X-API-Key: invalid-key" \
  -d '{"query": "test"}'
```
- [ ] Invalid key rejected with 401
- [ ] Valid key accepted

### 3. Admin Endpoint Tests
```bash
# Should return logs
curl http://localhost:8000/admin/logs \
  -H "X-API-Key: YOUR_ADMIN_KEY"
```
- [ ] Admin key works for `/admin/logs`
- [ ] User key rejected with 403

### 4. Automated Tests
```bash
python test_api.py
```
- [ ] All tests pass
- [ ] Health check: PASS
- [ ] Invalid key rejection: PASS
- [ ] Admin logs: PASS

---

## 📤 Data Upload Checklist

### 1. Upload First Document
```bash
curl -X POST http://localhost:8000/admin/upload-file \
  -H "X-API-Key: YOUR_ADMIN_KEY" \
  -F "file=@sample.pdf"
```

- [ ] File uploaded successfully
- [ ] `original_path` returned
- [ ] `extracted_path` returned
- [ ] `characters_extracted` > 0
- [ ] Background rebuild triggered

### 2. Verify File Storage
- [ ] Original saved to `data/policies/{domain}/{company}/`
- [ ] Text saved to `data/raw_data/{domain}/{company}/`
- [ ] Wait 10-30 seconds for rebuild
- [ ] Vector store created in `data/vector_stores/{domain}/{company}/`
- [ ] `vector.index` file exists
- [ ] `metadata.json` file exists

### 3. Add URL (Optional)
```bash
curl -X POST http://localhost:8000/admin/add-url \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_ADMIN_KEY" \
  -d '{"url": "https://example.com"}'
```

- [ ] URL fetched successfully
- [ ] Text saved to `raw_data/`
- [ ] Background rebuild triggered

---

## 💬 Chat Functionality Checklist

### 1. First Chat Request
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_USER_KEY" \
  -d '{"query": "What is your policy?"}'
```

Check response contains:
- [ ] `query` field
- [ ] `domain` field (matches your key)
- [ ] `company` field (matches your key)
- [ ] `sentiment` field (angry/neutral/happy)
- [ ] `sentiment_confidence` field (0.0-1.0)
- [ ] `response` field (AI-generated text)
- [ ] `response_time_ms` field
- [ ] `timestamp` field

### 2. Verify Logging
```bash
tail -20 logs/api.log
```

Check logs show:
- [ ] Chat request received
- [ ] Domain and company logged
- [ ] Sentiment detected
- [ ] Response time logged

### 3. Performance Check
- [ ] First request: 10-30 seconds (warmup)
- [ ] Second request: <2 seconds (cached)
- [ ] Sentiment confidence: >0.5
- [ ] Response makes sense

---

## 🔒 Security Checklist

### 1. API Key Security
- [ ] No default/example keys in production
- [ ] All keys are 32+ characters
- [ ] Keys use random characters (not dictionary words)
- [ ] `api_keys.json` NOT in git repository
- [ ] `.gitignore` includes `api_keys.json`

### 2. Access Control
- [ ] Admin keys separated from user keys
- [ ] User keys can only access their own domain/company
- [ ] Admin endpoints reject user keys (403)
- [ ] Invalid keys rejected (401)

### 3. Production Settings
- [ ] CORS configured (change `allow_origins` in src/server/main.py)
- [ ] HTTPS enabled (via reverse proxy)
- [ ] Rate limiting configured (nginx/middleware)
- [ ] Firewall allows only necessary ports

---

## 📊 Monitoring Checklist

### 1. Health Monitoring
Set up automated health checks:
- [ ] Cron job or monitoring service
- [ ] Check `/api/health` every 5 minutes
- [ ] Alert if `status != "healthy"`
- [ ] Alert if `vector_builder_active == false`

### 2. Log Monitoring
- [ ] `logs/api.log` rotating (use logrotate)
- [ ] Error monitoring (grep for ERROR/WARNING)
- [ ] Response time monitoring (check for slowdowns)
- [ ] Failed request monitoring (401/403/500 errors)

### 3. Resource Monitoring
- [ ] Memory usage: <80% (should be ~8GB)
- [ ] CPU usage: <50% (except during inference)
- [ ] Disk space: >20% free
- [ ] Process uptime tracking

---

## 🔄 Backup Checklist

### 1. Critical Files to Backup
- [ ] `api_keys.json` (store securely!)
- [ ] `data/policies/` directory (original documents)
- [ ] `domain_classifier.pkl`
- [ ] `adapters/` directory (.zip files)
- [ ] `logs/api.log` (for audit trail)

### 2. Backup Schedule
- [ ] Daily: `policies/` directory
- [ ] Weekly: Full backup including vector stores
- [ ] Monthly: Archive old logs

### 3. Recovery Test
- [ ] Restore from backup to test server
- [ ] Verify all files present
- [ ] Test API functionality
- [ ] Document recovery time

---

## 🚢 Production Deployment Checklist

### 1. Server Configuration
- [ ] Use Gunicorn/Uvicorn with multiple workers
- [ ] Configure worker timeout (120+ seconds)
- [ ] Set up reverse proxy (nginx/Apache)
- [ ] Configure SSL/TLS certificates
- [ ] Set up firewall rules

### 2. Process Management
- [ ] Use systemd/supervisor for auto-restart
- [ ] Configure log rotation
- [ ] Set resource limits
- [ ] Enable process monitoring

### 3. Performance Tuning
- [ ] GPU enabled (if available)
- [ ] Optimize worker count (2-4 workers recommended)
- [ ] Configure cache settings
- [ ] Enable compression (gzip)

---

## ✅ Final Launch Checklist

### Pre-Launch
- [ ] All tests passing
- [ ] Production API keys configured
- [ ] HTTPS enabled
- [ ] Monitoring active
- [ ] Backups configured
- [ ] Documentation reviewed
- [ ] Team trained on API usage

### Launch
- [ ] Start server with production config
- [ ] Verify health endpoint
- [ ] Test with real requests
- [ ] Monitor logs for errors
- [ ] Check resource usage

### Post-Launch (First 24 Hours)
- [ ] Monitor error rates
- [ ] Check response times
- [ ] Verify sentiment detection accuracy
- [ ] Review log files
- [ ] Test backup/restore
- [ ] Collect user feedback

---

## 📞 Troubleshooting Quick Reference

| Issue | Check | Solution |
|-------|-------|----------|
| Server won't start | `api_keys.json` | Create/fix JSON syntax |
| 401 errors | API key header | Use `X-API-Key` header |
| 404 on chat | Vector stores | Upload documents first |
| Slow responses | First request | Expected (model warmup) |
| Out of memory | RAM usage | Close apps, reduce workers |
| Sentiment always neutral | Model loading | Check logs for errors |

---

## 📚 Documentation Reference

- **API Endpoints**: See `docs/API.md`
- **Setup Guide**: See `docs/QUICKSTART.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Implementation**: See `docs/IMPLEMENTATION_SUMMARY.md`
- **Main README**: See `README.md`

---

## 🎯 Success Criteria

Your NexusAI deployment is successful when:

✅ Server starts in <60 seconds
✅ Health endpoint returns "healthy"
✅ All 3 LoRA adapters loaded
✅ Sentiment model active
✅ Vector builder running
✅ Chat requests respond in <2s
✅ Sentiment detection >80% confidence
✅ No errors in logs
✅ Backups configured
✅ Monitoring active

---

**When all checkboxes are complete, you're ready for production! 🎉**



