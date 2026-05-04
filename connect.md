# Connect NexusAI Frontend (BrozG/nexusai)

This guide shows how to connect the Next.js frontend to the FastAPI backend in this repo, even if your UI pages are incomplete.

## 1) Start the backend (this repo)

```bash
cd c:\brozfiles\project\LoRa-Vector-Bot\nexsusai-ml
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

Backend should be available at:

```
http://localhost:8000
```

Health check:

```bash
curl http://localhost:8000/api/health
```

## 2) Get your API key

Check api_keys.json in this repo. Example key:

```
sk_education_wikipedia_tes123
```

You can add a new key by editing api_keys.json and restarting the server.

## 3) Start the frontend (BrozG/nexusai)

```bash
git clone https://github.com/BrozG/nexusai
cd nexusai
npm install
```

Create .env.local:

```bash
FASTAPI_URL=http://localhost:8000
```

Run the UI:

```bash
npm run dev
```

Open:

```
http://localhost:3000
```

## 4) Update the Next.js API proxy

The frontend uses app/api/chat/route.ts to proxy requests to the backend. Make sure it sends the API key as X-API-Key and forwards only the fields the backend expects.

Example:

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

## 5) Frontend request body

From the UI, send:

```json
{
  "api_key": "sk_education_wikipedia_tes123",
  "query": "What is Wikipedia?",
  "top_k": 3,
  "max_tokens": 150,
  "temperature": 0.3
}
```

The backend derives domain and company from the key, so you do not need to send domain.

## 6) Optional: base vs adapter compare

If you want to show base vs LoRA in the UI, call /api/chat/compare instead of /api/chat:

```ts
const res = await fetch(`${process.env.FASTAPI_URL}/api/chat/compare`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
    'ngrok-skip-browser-warning': 'true'
  },
  body: JSON.stringify({ query, top_k, max_tokens, temperature })
})
```

Response fields:

- adapter_response
- base_response

## Troubleshooting

- 401 Invalid API key: confirm the key in api_keys.json and restart the backend after edits.
- 503 Model server error: backend is not running or FASTAPI_URL is wrong.
- Slow first request: model download and load can take a few minutes on first run.



