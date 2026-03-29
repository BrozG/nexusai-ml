# RAG Response Fixes (March 2026)

## Issues Fixed

### 1. Empty Responses from `/api/chat`

**Symptom:** API returned `"response": ""` (empty string)

**Root Cause:** Character-based string slicing instead of token-based extraction.

**Bad Code:**
```python
full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
answer = full_response[len(prompt):]  # Character slicing - WRONG!
```

**Problem:** The prompt and decoded output have different lengths because:
- Tokenization doesn't have 1:1 character mapping
- Special tokens affect the string differently

**Fix:** Use token-based extraction:
```python
input_length = inputs['input_ids'].shape[1]  # Number of input tokens
generated_tokens = outputs[0][input_length:]  # Slice tensor, not string
answer = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
```

**File:** `src/simple_rag.py` (lines 266-269)

---

### 2. Responses About Wrong Topics (ML Instead of Wikipedia)

**Symptom:** Asked about Wikipedia, got answers about machine learning and regression.

**Root Causes:**
1. **LoRA prompt format mismatch** - Prompts didn't match training format
2. **Irrelevant file in vector store** - `url_wiki_Machine_learning.txt` was retrieved for queries containing "works"
3. **Only 1 chunk used** - `top_k` parameter wasn't being used

#### Fix A: LoRA Prompt Format

Training data format (from `training/training_data/education.json`):
```json
{
  "instruction": "Answer the following question...",
  "input": "Question here",
  "output": "Answer here"
}
```

**Bad Prompt (generic LLM style):**
```python
prompt = f"""Answer this question based on the context:
Context: {context}
Question: {query}
Answer:"""
```

**Good Prompt (matches training):**
```python
prompt = f"""Instruction: Answer the following question using the context provided.
Context: {context}
Input: {query}
Output:"""
```

**File:** `src/simple_rag.py` (lines 228-236)

#### Fix B: Remove Polluting Data

Deleted: `data/raw_data/education/wikipedia/url_wiki_Machine_learning.txt`

This file contained irrelevant ML content that ranked high in vector search for queries containing "works", "how", "what" (common words).

**Solution for users:** Use `/api/files/{filename}` DELETE to remove irrelevant files. Vector store rebuilds automatically.

#### Fix C: Use All Retrieved Chunks

**Bad Code:**
```python
context = results[0]['text'] if results else ""  # Only first chunk!
```

**Good Code:**
```python
context_parts = []
for i, result in enumerate(results[:top_k], 1):
    context_parts.append(f"[Source {i}]: {result['text']}")
context = "\n\n".join(context_parts)
```

**File:** `src/simple_rag.py` (lines 207-216)

---

### 3. Partial/Truncated Responses

**Symptom:** Responses started mid-sentence or ended incomplete.

**Causes:**
- Input truncation at 256 tokens cut off the prompt start
- Response sometimes started with leftover context
- Sentence could end mid-word

**Fixes:**

1. **Increased max_length:** 256 → 1024 tokens for input
2. **Added response cleanup logic:**

```python
def _clean_response(self, response: str) -> str:
    """Remove partial sentences from start/end"""
    lines = response.strip().split('\n')
    cleaned_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        # Skip first line if it's a partial sentence
        if i == 0 and line[0].islower():
            continue
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Remove incomplete final sentence
    if text and not text.endswith(('.', '!', '?', '"', "'")):
        last_period = text.rfind('.')
        if last_period > len(text) * 0.5:  # Keep if >50% of content
            text = text[:last_period + 1]
    
    return text.strip()
```

**File:** `src/simple_rag.py` (lines 271-287)

---

## Configuration Changes

| Setting | Before | After | Reason |
|---------|--------|-------|--------|
| `max_length` | 256 | 1024 | Fit multiple chunks without truncation |
| `max_new_tokens` | 100 | 200 | Longer, more complete answers |
| `temperature` | 0.7 | 0.3 | More focused, less random |
| `top_k` default | 1 | 3 | Better context coverage |

---

## How LoRA Adapters Work

The system uses domain-specific LoRA adapters trained on customer support data:

```
adapters/
├── ecommerce_adapter/    # Amazon, Flipkart, etc.
├── education_adapter/    # Wikipedia, schools, etc.
└── telecom_adapter/      # Airtel, Jio, etc.
```

**Key Point:** LoRA adapters are trained with specific prompt formats. Using the wrong format makes the model ignore its training and produce generic outputs.

**Training Format Expected:**
```
Instruction: <task description>
Context: <relevant content>
Input: <user question>
Output: <expected answer>
```

---

## Data Quality Tips

1. **Upload comprehensive documents** (500+ words each)
2. **Avoid duplicate/overlapping content** - Confuses retrieval
3. **Remove irrelevant files** - Use DELETE endpoints
4. **Check vector store** - Files are chunked at 450 words

### Symptoms of Data Pollution

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Wrong topic in answer | Irrelevant file retrieved | Delete file, rebuild vectors |
| Generic/vague answers | Too little content | Upload more detailed docs |
| Contradictory answers | Conflicting sources | Remove outdated files |
| Partial sentences | Content too fragmented | Use larger documents |

---

## Testing Fixes

After making changes, test with:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_education_wikipedia_tes123" \
  -d '{
    "query": "Who founded Wikipedia and what are its content policies?",
    "top_k": 3,
    "max_tokens": 200
  }'
```

**Expected:**
- Response mentions Jimmy Wales, Larry Sanger
- Discusses Wikipedia's policies (neutrality, verifiability)
- Sentiment: neutral (not angry)
- Response time: 30-120 seconds (CPU)

---

## Files Modified

| File | Changes |
|------|---------|
| `src/simple_rag.py` | Token extraction, prompt format, chunking, cleanup |
| `src/main.py` | File/URL management endpoints, Swagger auth |
| `data/raw_data/education/wikipedia/` | Removed polluting ML file |

---

## Future Improvements

For production deployment:

1. **GPU acceleration** - 10-20x faster inference
2. **Async processing** - Queue long-running requests
3. **Caching** - Cache frequent queries
4. **Streaming** - Return tokens as generated
5. **Chunking improvements** - Semantic chunking instead of word-based
