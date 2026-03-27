"""
NexusAI FastAPI Server
Integrates all components: RAG, PDF handling, web scraping, vector building
"""

import json
import logging
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
import asyncio

from fastapi import FastAPI, HTTPException, File, UploadFile, Header, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging ONCE for the entire application
# Do this BEFORE any Windows console encoding fixes
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Create console handler with UTF-8 encoding support
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Create file handler
file_handler = logging.FileHandler(log_dir / 'api.log', encoding='utf-8', mode='a')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Only add handlers if not already configured
if not root_logger.handlers:
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

# Fix Windows console encoding AFTER logging is configured
# This prevents conflicts with logging handlers
if sys.platform == "win32":
    try:
        import io
        import codecs
        # Only wrap if not already wrapped
        if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        if not isinstance(sys.stderr, io.TextIOWrapper) or sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except Exception as e:
        logger.warning(f"Could not set UTF-8 encoding for console: {e}")

# Import local modules
try:
    from src.simple_rag import SimpleRAG
    from src.pdf_handler import handle_pdf_with_original
    from src.universal_fetcher import UniversalFetcher
    from src.vector_builder import VectorStoreBuilder, watch_mode
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    # Try relative imports (when running from src/)
    try:
        from simple_rag import SimpleRAG
        from pdf_handler import handle_pdf_with_original
        from universal_fetcher import UniversalFetcher
        from vector_builder import VectorStoreBuilder, watch_mode
        DEPENDENCIES_AVAILABLE = True
    except ImportError as e:
        logger.error(f"Failed to import local modules: {e}")
        DEPENDENCIES_AVAILABLE = False

# Try to import sentiment model
try:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    import torch
    SENTIMENT_AVAILABLE = True
except ImportError:
    logger.warning("Sentiment analysis dependencies not available")
    SENTIMENT_AVAILABLE = False


# ============================================================================
# MODELS
# ============================================================================

class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    query: str
    domain: str
    company: str
    sentiment: str
    sentiment_confidence: float
    response: str
    response_time_ms: float
    timestamp: str


class UploadResponse(BaseModel):
    success: bool
    message: str
    domain: str
    company: str
    original_path: Optional[str] = None
    extracted_path: Optional[str] = None
    characters_extracted: Optional[int] = None


class URLRequest(BaseModel):
    url: str


class URLResponse(BaseModel):
    success: bool
    message: str
    domain: str
    company: str
    url: str


class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    loaded_adapters: List[str]
    sentiment_model_loaded: bool
    vector_builder_active: bool
    timestamp: str


# ============================================================================
# GLOBAL STATE
# ============================================================================

class AppState:
    """Global application state"""
    def __init__(self):
        self.api_keys: Dict = {}
        self.admin_keys: List[str] = []
        self.rag: Optional[SimpleRAG] = None
        self.sentiment_model = None
        self.sentiment_tokenizer = None
        self.fetcher: Optional[UniversalFetcher] = None
        self.vector_builder: Optional[VectorStoreBuilder] = None
        self.vector_builder_thread: Optional[threading.Thread] = None
        self.start_time = time.time()
        self.loaded_adapters: List[str] = []

app_state = AppState()


# ============================================================================
# STARTUP
# ============================================================================

# Project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent


def load_api_keys():
    """Load API keys configuration"""
    api_keys_file = PROJECT_ROOT / "api_keys.json"
    
    if not api_keys_file.exists():
        logger.error("api_keys.json not found! Creating template...")
        template = {
            "api_keys": {
                "sk_example_key_123": {
                    "domain": "ecommerce",
                    "company": "amazon",
                    "role": "user",
                    "description": "Example API Key"
                }
            },
            "admin_keys": ["sk_admin_master_xyz999"]
        }
        with open(api_keys_file, 'w') as f:
            json.dump(template, f, indent=2)
        raise RuntimeError("api_keys.json created. Please configure your keys.")
    
    with open(api_keys_file, 'r') as f:
        config = json.load(f)
    
    app_state.api_keys = config.get("api_keys", {})
    app_state.admin_keys = config.get("admin_keys", [])
    
    logger.info(f"Loaded {len(app_state.api_keys)} API keys")
    logger.info(f"Loaded {len(app_state.admin_keys)} admin keys")


def clear_old_logs():
    """Clear old log file on startup"""
    log_file = PROJECT_ROOT / "logs" / "api.log"
    if log_file.exists():
        try:
            # Clear the file content
            with open(log_file, 'w') as f:
                f.write("")
            logger.info("Previous log file cleared")
        except Exception as e:
            logger.warning(f"Could not clear old logs: {e}")


def load_sentiment_model():
    """Load sentiment analysis model"""
    if not SENTIMENT_AVAILABLE:
        logger.warning("Sentiment analysis not available - skipping")
        return
    
    try:
        logger.info("Loading sentiment model: cardiffnlp/twitter-roberta-base-sentiment-latest")
        app_state.sentiment_tokenizer = AutoTokenizer.from_pretrained(
            "cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        app_state.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
            "cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        app_state.sentiment_model.eval()
        logger.info("✓ Sentiment model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load sentiment model: {e}")


def load_rag_system():
    """Load RAG system with all adapters"""
    if not DEPENDENCIES_AVAILABLE:
        logger.error("Dependencies not available - RAG system cannot load")
        return
    
    try:
        logger.info("Initializing RAG system...")
        app_state.rag = SimpleRAG()
        
        # Pre-load all adapters
        logger.info("Pre-loading LoRA adapters...")
        domains = ["ecommerce", "education", "telecom"]
        
        for domain in domains:
            try:
                logger.info(f"Loading {domain} adapter...")
                app_state.rag._load_lora_adapter(domain)
                app_state.loaded_adapters.append(domain)
                logger.info(f"✓ {domain} adapter loaded")
            except Exception as e:
                logger.error(f"Failed to load {domain} adapter: {e}")
        
        logger.info(f"✓ RAG system ready with {len(app_state.loaded_adapters)} adapters")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")


def start_vector_builder_watch():
    """Start vector builder in watch mode as background thread"""
    if not DEPENDENCIES_AVAILABLE:
        logger.warning("Dependencies not available - vector builder not started")
        return
    
    try:
        logger.info("Starting vector builder in watch mode...")
        app_state.vector_builder = VectorStoreBuilder()
        
        # Run watch mode in separate thread with proper error handling
        def run_watch():
            try:
                # Give main thread time to fully initialize
                time.sleep(2)
                logger.info("Vector builder watch thread starting...")
                watch_mode(app_state.vector_builder)
            except Exception as e:
                logger.error(f"Vector builder watch mode crashed: {e}", exc_info=True)
        
        app_state.vector_builder_thread = threading.Thread(
            target=run_watch,
            daemon=True,
            name="VectorBuilderWatch"
        )
        app_state.vector_builder_thread.start()
        logger.info("✓ Vector builder watch mode thread started (will activate after 2s delay)")
    except Exception as e:
        logger.error(f"Failed to start vector builder: {e}", exc_info=True)


def initialize_components():
    """Initialize fetcher and other components"""
    try:
        app_state.fetcher = UniversalFetcher()
        logger.info("✓ Universal fetcher initialized")
    except Exception as e:
        logger.error(f"Failed to initialize fetcher: {e}")


# ============================================================================
# AUTHENTICATION
# ============================================================================

def validate_api_key(x_api_key: Optional[str] = Header(None)) -> Dict:
    """Validate API key and return domain/company info"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    
    if x_api_key not in app_state.api_keys:
        logger.warning(f"Invalid API key attempted: {x_api_key[:10]}...")
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return app_state.api_keys[x_api_key]


def validate_admin_key(x_api_key: Optional[str] = Header(None)) -> Dict:
    """Validate admin API key"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    
    if x_api_key not in app_state.admin_keys:
        logger.warning(f"Invalid admin key attempted: {x_api_key[:10]}...")
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Return admin key info
    return app_state.api_keys.get(x_api_key, {
        "domain": "admin",
        "company": "admin",
        "role": "admin"
    })


# ============================================================================
# SENTIMENT ANALYSIS
# ============================================================================

def detect_sentiment(text: str) -> tuple[str, float]:
    """
    Detect sentiment of text
    Returns: (label, confidence)
    """
    if not SENTIMENT_AVAILABLE or app_state.sentiment_model is None:
        return ("neutral", 0.0)
    
    try:
        # Tokenize
        inputs = app_state.sentiment_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        
        # Get prediction
        with torch.no_grad():
            outputs = app_state.sentiment_model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)[0]
        
        # Labels: negative, neutral, positive
        labels = ["negative", "neutral", "positive"]
        predicted_idx = torch.argmax(scores).item()
        confidence = scores[predicted_idx].item()
        
        # Map negative to angry, positive to happy
        label_map = {
            "negative": "angry",
            "neutral": "neutral",
            "positive": "happy"
        }
        
        sentiment = label_map[labels[predicted_idx]]
        
        return (sentiment, confidence)
    
    except Exception as e:
        logger.error(f"Sentiment detection failed: {e}")
        return ("neutral", 0.0)


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="NexusAI API",
    description="AI-powered customer support with RAG and LoRA fine-tuned models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Run on server startup"""
    # Clear old logs first
    clear_old_logs()
    
    logger.info("=" * 70)
    logger.info("NexusAI API Server Starting...")
    logger.info("=" * 70)
    
    try:
        # Load components in order
        logger.info("Step 1/5: Loading API keys...")
        load_api_keys()
        
        logger.info("Step 2/5: Loading sentiment model...")
        load_sentiment_model()
        
        logger.info("Step 3/5: Initializing RAG system...")
        load_rag_system()
        
        logger.info("Step 4/5: Initializing components...")
        initialize_components()
        
        logger.info("Step 5/5: Starting vector builder watch mode...")
        start_vector_builder_watch()
        
        logger.info("=" * 70)
        logger.info("✓ Server startup complete!")
        logger.info(f"✓ Loaded adapters: {app_state.loaded_adapters}")
        logger.info(f"✓ Sentiment model: {'Active' if app_state.sentiment_model else 'Disabled'}")
        logger.info(f"✓ Vector builder: {'Active' if app_state.vector_builder_thread else 'Disabled'}")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Run on server shutdown"""
    logger.info("Server shutting down...")


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    key_info: Dict = Depends(validate_api_key)
):
    """
    Main chat endpoint with sentiment detection and RAG
    """
    start_time = time.time()
    
    domain = key_info["domain"]
    company = key_info["company"]
    query = request.query
    
    logger.info(f"Chat request - Domain: {domain}, Company: {company}, Query: {query[:50]}...")
    
    # Check if RAG is available
    if app_state.rag is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Detect sentiment
        sentiment, sentiment_conf = detect_sentiment(query)
        logger.info(f"Sentiment: {sentiment} (confidence: {sentiment_conf:.3f})")
        
        # Generate response using RAG
        result = app_state.rag.generate(
            query=query,
            domain=domain,
            company=company,
            top_k=request.top_k,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        response_time_ms = (time.time() - start_time) * 1000
        
        # Log the interaction
        logger.info(f"Response generated in {response_time_ms:.2f}ms - Sentiment: {sentiment}")
        
        return ChatResponse(
            query=query,
            domain=domain,
            company=company,
            sentiment=sentiment,
            sentiment_confidence=sentiment_conf,
            response=result["answer"],
            response_time_ms=response_time_ms,
            timestamp=datetime.now().isoformat()
        )
    
    except FileNotFoundError as e:
        logger.error(f"Vector store not found: {e}")
        raise HTTPException(
            status_code=404,
            detail=f"Vector store not found for {domain}/{company}. Please upload documents first."
        )
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.post("/admin/upload-file", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    key_info: Dict = Depends(validate_api_key)
):
    """
    Upload PDF/DOCX/TXT file and process it
    Any valid API key can upload - domain/company automatically determined from the key
    """
    # Extract domain and company from API key
    domain = key_info["domain"]
    company = key_info["company"]
    
    logger.info(f"File upload - Domain: {domain}, Company: {company}, File: {file.filename}")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Process with pdf_handler
        result = handle_pdf_with_original(
            file=file_content,
            domain=domain,
            company=company,
            filename=file.filename
        )
        
        if result["success"]:
            # Trigger vector store rebuild in background
            def rebuild_vector_store():
                try:
                    if app_state.vector_builder:
                        logger.info(f"Rebuilding vector store for {domain}/{company}")
                        app_state.vector_builder.build_vector_store(domain, company)
                        logger.info(f"✓ Vector store rebuilt for {domain}/{company}")
                except Exception as e:
                    logger.error(f"Failed to rebuild vector store: {e}")
            
            background_tasks.add_task(rebuild_vector_store)
            
            logger.info(f"✓ File uploaded successfully: {file.filename}")
            
            return UploadResponse(
                success=True,
                message=f"File processed successfully",
                domain=domain,
                company=company,
                original_path=result.get("original_path"),
                extracted_path=result.get("extracted_path"),
                characters_extracted=result.get("characters_extracted")
            )
        else:
            raise HTTPException(status_code=400, detail=result.get("message", "Processing failed"))
    
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/admin/add-url", response_model=URLResponse)
async def add_url(
    request: URLRequest,
    background_tasks: BackgroundTasks,
    key_info: Dict = Depends(validate_api_key)
):
    """
    Add URL to scrape and process
    Any valid API key can add URLs - domain/company automatically determined from the key
    """
    # Extract domain and company from API key
    domain = key_info["domain"]
    company = key_info["company"]
    
    logger.info(f"URL add - Domain: {domain}, Company: {company}, URL: {request.url}")
    
    try:
        if app_state.fetcher is None:
            raise HTTPException(status_code=503, detail="Fetcher not initialized")
        
        # Fetch URL
        success = app_state.fetcher.fetch_url(domain, company, request.url)
        
        if success:
            # Trigger vector store rebuild in background
            def rebuild_vector_store():
                try:
                    if app_state.vector_builder:
                        logger.info(f"Rebuilding vector store for {domain}/{company}")
                        app_state.vector_builder.build_vector_store(domain, company)
                        logger.info(f"✓ Vector store rebuilt for {domain}/{company}")
                except Exception as e:
                    logger.error(f"Failed to rebuild vector store: {e}")
            
            background_tasks.add_task(rebuild_vector_store)
            
            logger.info(f"✓ URL processed successfully: {request.url}")
            
            return URLResponse(
                success=True,
                message="URL fetched and processed successfully",
                domain=domain,
                company=company,
                url=request.url
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch URL")
    
    except Exception as e:
        logger.error(f"URL fetch error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"URL fetch failed: {str(e)}")


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - no authentication required
    """
    uptime = time.time() - app_state.start_time
    
    return HealthResponse(
        status="healthy" if app_state.rag else "degraded",
        uptime_seconds=uptime,
        loaded_adapters=app_state.loaded_adapters,
        sentiment_model_loaded=app_state.sentiment_model is not None,
        vector_builder_active=app_state.vector_builder_thread is not None and app_state.vector_builder_thread.is_alive(),
        timestamp=datetime.now().isoformat()
    )


@app.get("/admin/logs")
async def get_logs(
    lines: int = 100,
    key_info: Dict = Depends(validate_admin_key)
):
    """
    Get last N lines of API log
    Admin only
    """
    log_file = Path("logs/api.log")
    
    if not log_file.exists():
        return {"lines": [], "count": 0}
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        # Get last N lines
        last_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return {
            "lines": [line.strip() for line in last_lines],
            "count": len(last_lines),
            "total_lines": len(all_lines)
        }
    
    except Exception as e:
        logger.error(f"Failed to read logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to read logs")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "NexusAI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "POST /api/chat",
            "upload": "POST /admin/upload-file",
            "add_url": "POST /admin/add-url",
            "health": "GET /api/health",
            "logs": "GET /admin/logs"
        }
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point for the server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NexusAI FastAPI Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    logger.info(f"Starting server on {args.host}:{args.port}")
    
    uvicorn.run(
        "src.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
