"""
Vector Store Builder with File Monitoring
Automatically builds and updates FAISS vector stores from raw text data.
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configure logging only if running as main script (not when imported by main.py)
# This prevents conflicts when used as a module
if __name__ == "__main__":
    # Fix Windows console encoding for Unicode characters
    if sys.platform == "win32":
        try:
            import io
            if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            if not isinstance(sys.stderr, io.TextIOWrapper) or sys.stderr.encoding != 'utf-8':
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        except Exception:
            pass
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('vector_builder.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)

# Optional imports with availability flags
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logger.error("numpy not installed. Run: pip install numpy")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.error("faiss-cpu not installed. Run: pip install faiss-cpu")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.error("sentence-transformers not installed. Run: pip install sentence-transformers")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    logger.warning("watchdog not installed. Run: pip install watchdog")

    # Create dummy base class if watchdog not available
    class FileSystemEventHandler:
        """Dummy class when watchdog is not available."""
        pass


class TextChunker:
    """Handles text chunking with overlap."""

    def __init__(self, chunk_size: int = 450, overlap: int = 50):
        """
        Initialize chunker.

        Args:
            chunk_size: Target chunk size in words (400-500 range)
            overlap: Number of overlapping words between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, source_file: str) -> List[Dict]:
        """
        Split text into overlapping chunks.

        Args:
            text: Input text to chunk
            source_file: Source filename for metadata

        Returns:
            List of dicts with chunk text and metadata
        """
        words = text.split()
        chunks = []
        chunk_id = 0

        # Handle empty or very short text
        if len(words) < self.overlap:
            if words:
                return [{
                    "text": text.strip(),
                    "source": source_file,
                    "chunk_id": 0,
                    "word_count": len(words),
                    "start_word": 0,
                    "end_word": len(words)
                }]
            return []

        start = 0
        while start < len(words):
            # Calculate end position
            end = min(start + self.chunk_size, len(words))

            # Extract chunk
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)

            chunks.append({
                "text": chunk_text.strip(),
                "source": source_file,
                "chunk_id": chunk_id,
                "word_count": len(chunk_words),
                "start_word": start,
                "end_word": end
            })

            chunk_id += 1

            # Move to next chunk with overlap
            start += self.chunk_size - self.overlap

            # Break if we've processed all words
            if end >= len(words):
                break

        return chunks


class VectorStoreBuilder:
    """Builds and manages FAISS vector stores."""

    def __init__(
        self,
        base_dir: str = None,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        # Default to project root (parent of src/)
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parents[2]
        else:
            self.base_dir = Path(base_dir)
        
        # Data directories are now in data/
        self.raw_data_dir = self.base_dir / "data" / "raw_data"
        self.vector_stores_dir = self.base_dir / "data" / "vector_stores"
        self.model_name = model_name
        self.embedding_model = None
        self.chunker = TextChunker(chunk_size=450, overlap=50)

    def _load_embedding_model(self):
        """Load sentence transformer model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.error("sentence-transformers not available")
            return False

        if self.embedding_model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            try:
                self.embedding_model = SentenceTransformer(self.model_name)
                logger.info(f"Model loaded successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                return False
        return True

    def _ensure_directory(self, domain: str, company: str) -> Path:
        """Create vector store directory."""
        output_path = self.vector_stores_dir / domain / company
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path

    def _read_text_files(self, domain: str, company: str) -> List[Tuple[str, str]]:
        """
        Read all .txt files for a company.

        Returns:
            List of (filename, content) tuples
        """
        company_dir = self.raw_data_dir / domain / company

        if not company_dir.exists():
            logger.warning(f"Directory not found: {company_dir}")
            return []

        text_files = []
        for txt_file in company_dir.glob("*.txt"):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        text_files.append((txt_file.name, content))
                        logger.info(f"Read {len(content)} chars from {txt_file.name}")
            except Exception as e:
                logger.error(f"Failed to read {txt_file}: {e}")

        return text_files

    def build_vector_store(self, domain: str, company: str) -> Dict:
        """
        Build vector store for a specific company.

        Args:
            domain: Domain category
            company: Company name

        Returns:
            Dict with build status and stats
        """
        logger.info(f"Building vector store for {domain}/{company}")

        # Check dependencies
        if not all([NUMPY_AVAILABLE, FAISS_AVAILABLE, SENTENCE_TRANSFORMERS_AVAILABLE]):
            return {
                "success": False,
                "message": "Missing required dependencies",
                "domain": domain,
                "company": company
            }

        # Load model
        if not self._load_embedding_model():
            return {
                "success": False,
                "message": "Failed to load embedding model",
                "domain": domain,
                "company": company
            }

        # Read all text files
        text_files = self._read_text_files(domain, company)

        if not text_files:
            logger.warning(f"No text files found for {domain}/{company}")
            return {
                "success": False,
                "message": "No text files found",
                "domain": domain,
                "company": company
            }

        # Chunk all texts
        all_chunks = []
        for filename, content in text_files:
            chunks = self.chunker.chunk_text(content, filename)
            all_chunks.extend(chunks)

        if not all_chunks:
            return {
                "success": False,
                "message": "No chunks generated",
                "domain": domain,
                "company": company
            }

        logger.info(f"Generated {len(all_chunks)} chunks from {len(text_files)} files")

        # Extract chunk texts for embedding
        chunk_texts = [chunk["text"] for chunk in all_chunks]

        # Generate embeddings
        logger.info("Generating embeddings...")
        try:
            embeddings = self.embedding_model.encode(
                chunk_texts,
                show_progress_bar=True,
                convert_to_numpy=True
            )
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return {
                "success": False,
                "message": f"Embedding generation failed: {e}",
                "domain": domain,
                "company": company
            }

        # Build FAISS index
        logger.info("Building FAISS index...")
        try:
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings.astype('float32'))
            logger.info(f"Index built with {index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Failed to build FAISS index: {e}")
            return {
                "success": False,
                "message": f"Index building failed: {e}",
                "domain": domain,
                "company": company
            }

        # Ensure output directory
        output_dir = self._ensure_directory(domain, company)

        # Save index
        index_file = output_dir / "vector.index"
        try:
            faiss.write_index(index, str(index_file))
            logger.info(f"Saved index to {index_file}")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            return {
                "success": False,
                "message": f"Failed to save index: {e}",
                "domain": domain,
                "company": company
            }

        # Prepare metadata
        metadata = {
            "domain": domain,
            "company": company,
            "created_at": datetime.now().isoformat(),
            "model_name": self.model_name,
            "embedding_dimension": dimension,
            "total_chunks": len(all_chunks),
            "total_files": len(text_files),
            "chunk_config": {
                "chunk_size": self.chunker.chunk_size,
                "overlap": self.chunker.overlap
            },
            "source_files": [f for f, _ in text_files],
            "chunks": all_chunks
        }

        # Save metadata
        metadata_file = output_dir / "metadata.json"
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved metadata to {metadata_file}")
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            return {
                "success": False,
                "message": f"Failed to save metadata: {e}",
                "domain": domain,
                "company": company
            }

        return {
            "success": True,
            "message": f"Successfully built vector store",
            "domain": domain,
            "company": company,
            "stats": {
                "files": len(text_files),
                "chunks": len(all_chunks),
                "dimension": dimension,
                "index_path": str(index_file.relative_to(self.base_dir)),
                "metadata_path": str(metadata_file.relative_to(self.base_dir))
            }
        }

    def build_all(self) -> Dict[str, int]:
        """
        Build vector stores for all companies in all domains.

        Returns:
            Statistics dict
        """
        stats = {
            "total_companies": 0,
            "successful": 0,
            "failed": 0,
            "details": []
        }

        logger.info("Starting full rebuild of all vector stores...")

        if not self.raw_data_dir.exists():
            logger.warning(f"Raw data directory not found: {self.raw_data_dir}")
            return stats

        # Iterate through all domains and companies
        for domain_dir in sorted(self.raw_data_dir.iterdir()):
            if not domain_dir.is_dir():
                continue

            domain = domain_dir.name

            for company_dir in sorted(domain_dir.iterdir()):
                if not company_dir.is_dir():
                    continue

                company = company_dir.name
                stats["total_companies"] += 1

                logger.info(f"\n{'='*60}")
                logger.info(f"Processing: {domain}/{company}")
                logger.info(f"{'='*60}")

                result = self.build_vector_store(domain, company)

                if result["success"]:
                    stats["successful"] += 1
                    logger.info(f"✓ Success: {domain}/{company}")
                else:
                    stats["failed"] += 1
                    logger.warning(f"✗ Failed: {domain}/{company} - {result['message']}")

                stats["details"].append(result)

        return stats

    def parse_path(self, file_path: str) -> Optional[Tuple[str, str]]:
        """
        Extract domain and company from file path.

        Args:
            file_path: Path to .txt file

        Returns:
            (domain, company) tuple or None
        """
        try:
            path = Path(file_path)

            # Check if it's in raw_data
            if "raw_data" not in path.parts:
                return None

            # Find raw_data index
            parts = path.parts
            raw_data_idx = parts.index("raw_data")

            # Check if we have domain and company
            if len(parts) > raw_data_idx + 2:
                domain = parts[raw_data_idx + 1]
                company = parts[raw_data_idx + 2]
                return (domain, company)

        except Exception as e:
            logger.error(f"Failed to parse path {file_path}: {e}")

        return None


class RawDataWatcher(FileSystemEventHandler):
    """Watches raw_data directory for changes."""

    def __init__(self, builder: VectorStoreBuilder):
        self.builder = builder
        self.last_rebuild = {}  # Track last rebuild time per company
        self.debounce_seconds = 5  # Wait 5 seconds before rebuilding

    def should_rebuild(self, domain: str, company: str) -> bool:
        """Check if enough time has passed since last rebuild."""
        key = f"{domain}/{company}"
        last_time = self.last_rebuild.get(key, 0)
        current_time = time.time()

        if current_time - last_time > self.debounce_seconds:
            self.last_rebuild[key] = current_time
            return True
        return False

    def on_created(self, event):
        """Handle file creation."""
        if event.is_directory:
            return

        if event.src_path.endswith('.txt'):
            self.handle_change(event.src_path, "created")

    def on_modified(self, event):
        """Handle file modification."""
        if event.is_directory:
            return

        if event.src_path.endswith('.txt'):
            self.handle_change(event.src_path, "modified")

    def handle_change(self, file_path: str, event_type: str):
        """Handle file change event."""
        logger.info(f"File {event_type}: {file_path}")

        # Parse domain and company from path
        parsed = self.builder.parse_path(file_path)

        if parsed is None:
            logger.warning(f"Could not parse domain/company from: {file_path}")
            return

        domain, company = parsed

        # Debounce - avoid rebuilding too frequently
        if not self.should_rebuild(domain, company):
            logger.info(f"Debouncing rebuild for {domain}/{company}")
            return

        # Rebuild vector store
        logger.info(f"Triggering rebuild for {domain}/{company}")
        result = self.builder.build_vector_store(domain, company)

        if result["success"]:
            logger.info(f"✓ Rebuilt vector store for {domain}/{company}")
        else:
            logger.warning(f"✗ Failed to rebuild: {result['message']}")


def watch_mode(builder: VectorStoreBuilder):
    """Run in watch mode with file monitoring."""
    if not WATCHDOG_AVAILABLE:
        logger.error("watchdog not installed. Run: pip install watchdog")
        print("\n✗ Watch mode requires watchdog. Install with:")
        print("  pip install watchdog")
        sys.exit(1)

    logger.info("Starting watch mode...")
    logger.info(f"Monitoring: {builder.raw_data_dir}")

    # Create event handler and observer
    event_handler = RawDataWatcher(builder)
    observer = Observer()
    observer.schedule(event_handler, str(builder.raw_data_dir), recursive=True)

    # Start observer
    observer.start()
    logger.info("File monitoring active. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file monitoring...")
        observer.stop()

    observer.join()
    logger.info("Watch mode stopped")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Vector Store Builder - Build and monitor FAISS vector stores',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build all vector stores once
  python src/vector/vector_builder.py --build

  # Watch for changes and auto-rebuild
  python src/vector/vector_builder.py --watch

  # Use custom embedding model
  python src/vector/vector_builder.py --build --model sentence-transformers/all-mpnet-base-v2
        """
    )

    parser.add_argument('--build', action='store_true', help='Build all vector stores (one-time)')
    parser.add_argument('--watch', action='store_true', help='Watch raw_data/ and auto-rebuild on changes')
    parser.add_argument('--model', type=str, default='all-MiniLM-L6-v2', help='Sentence transformer model name')

    args = parser.parse_args()

    # Create builder
    builder = VectorStoreBuilder(model_name=args.model)

    # Handle modes
    if args.watch:
        watch_mode(builder)

    elif args.build:
        stats = builder.build_all()

        print("\n" + "="*60)
        print("BUILD SUMMARY")
        print("="*60)
        print(f"Total companies: {stats['total_companies']}")
        print(f"Successful:      {stats['successful']}")
        print(f"Failed:          {stats['failed']}")
        print("="*60)

        # Show details
        if stats['details']:
            print("\nDetails:")
            for detail in stats['details']:
                status = "✓" if detail["success"] else "✗"
                print(f"  {status} {detail['domain']}/{detail['company']}")
                if detail["success"] and "stats" in detail:
                    s = detail["stats"]
                    print(f"      Files: {s['files']}, Chunks: {s['chunks']}, Dim: {s['dimension']}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

