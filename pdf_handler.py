"""
PDF/DOCX/TXT Handler for Document Processing
Extracts clean text from various document formats and saves to raw_data.
"""

import logging
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Union, BinaryIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Optional imports with availability flags
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


class DocumentHandler:
    """Handles document processing and text extraction."""

    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.raw_data_dir = self.base_dir / "raw_data"

    def _ensure_directory(self, domain: str, company: str) -> Path:
        """Create necessary directory structure."""
        output_path = self.raw_data_dir / domain / company
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path

    def _clean_filename(self, filename: str) -> str:
        """Extract clean filename without extension."""
        # Remove extension
        name = Path(filename).stem

        # Clean special characters
        name = re.sub(r'[^\w\-_]', '_', name)
        name = re.sub(r'_+', '_', name)
        name = name[:100]  # Limit length

        return name if name else 'document'

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""

        # Remove excessive whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned = '\n'.join(lines)

        # Remove excessive newlines
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

        # Remove control characters except newlines and tabs
        cleaned = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', cleaned)

        return cleaned.strip()

    def _extract_pdf(self, file_content: bytes) -> Optional[str]:
        """Extract text from PDF file."""
        if not PDF_AVAILABLE:
            logger.error("PyPDF2 not installed. Run: pip install PyPDF2")
            return None

        try:
            import io
            pdf_file = io.BytesIO(file_content)
            reader = PyPDF2.PdfReader(pdf_file)

            text_parts = []
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                except Exception as e:
                    logger.warning(f"Failed to extract page {page_num}: {e}")
                    continue

            full_text = '\n'.join(text_parts)
            logger.info(f"Extracted {len(full_text)} characters from {len(reader.pages)} pages")

            return full_text

        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            return None

    def _extract_docx(self, file_content: bytes) -> Optional[str]:
        """Extract text from DOCX file."""
        if not DOCX_AVAILABLE:
            logger.error("python-docx not installed. Run: pip install python-docx")
            return None

        try:
            import io
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)

            text_parts = []

            # Extract paragraphs
            for para in doc.paragraphs:
                if para.text.strip():
                    text_parts.append(para.text)

            # Extract tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = ' | '.join(cell.text.strip() for cell in row.cells)
                    if row_text.strip():
                        text_parts.append(row_text)

            full_text = '\n'.join(text_parts)
            logger.info(f"Extracted {len(full_text)} characters from DOCX")

            return full_text

        except Exception as e:
            logger.error(f"DOCX extraction failed: {e}")
            return None

    def _extract_txt(self, file_content: bytes) -> Optional[str]:
        """Extract text from TXT file."""
        try:
            # Try UTF-8 first, fallback to latin-1
            try:
                text = file_content.decode('utf-8')
            except UnicodeDecodeError:
                text = file_content.decode('latin-1', errors='ignore')

            logger.info(f"Extracted {len(text)} characters from TXT")
            return text

        except Exception as e:
            logger.error(f"TXT extraction failed: {e}")
            return None

    def process_file(
        self,
        file_content: bytes,
        filename: str,
        domain: str,
        company: str
    ) -> Dict[str, Union[bool, str]]:
        """
        Process a document file and save extracted text.

        Args:
            file_content: File content as bytes
            filename: Original filename with extension
            domain: Domain category (e.g., 'ecommerce', 'education', 'telecom')
            company: Company name

        Returns:
            Dict with status, message, and output_path
        """
        try:
            # Validate file extension
            file_ext = Path(filename).suffix.lower()
            if file_ext not in self.SUPPORTED_EXTENSIONS:
                return {
                    "success": False,
                    "message": f"Unsupported file type: {file_ext}. Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}",
                    "output_path": None
                }

            # Extract text based on file type
            if file_ext == '.pdf':
                text = self._extract_pdf(file_content)
            elif file_ext == '.docx':
                text = self._extract_docx(file_content)
            elif file_ext == '.txt':
                text = self._extract_txt(file_content)
            else:
                return {
                    "success": False,
                    "message": f"Unknown file type: {file_ext}",
                    "output_path": None
                }

            if text is None:
                return {
                    "success": False,
                    "message": f"Failed to extract text from {filename}",
                    "output_path": None
                }

            # Clean extracted text
            cleaned_text = self._clean_text(text)

            if not cleaned_text:
                return {
                    "success": False,
                    "message": "No text content found in file",
                    "output_path": None
                }

            # Prepare output path
            output_dir = self._ensure_directory(domain, company)
            clean_name = self._clean_filename(filename)
            output_file = output_dir / f"pdf_{clean_name}.txt"

            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            logger.info(f"Saved {len(cleaned_text)} characters to {output_file}")

            return {
                "success": True,
                "message": f"Successfully processed {filename}",
                "output_path": str(output_file.relative_to(self.base_dir)),
                "characters_extracted": len(cleaned_text)
            }

        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            return {
                "success": False,
                "message": f"Processing error: {str(e)}",
                "output_path": None
            }


# Convenience function for FastAPI integration
def handle_pdf(
    file: Union[bytes, BinaryIO],
    domain: str,
    company: str,
    filename: Optional[str] = None
) -> Dict[str, Union[bool, str]]:
    """
    Handle PDF/DOCX/TXT file upload and extraction.

    Args:
        file: File content as bytes or file-like object
        domain: Domain category
        company: Company name
        filename: Original filename (required if file is bytes)

    Returns:
        Dict with success status, message, and output path

    Example:
        >>> result = handle_pdf(file_bytes, "ecommerce", "amazon", "catalog.pdf")
        >>> if result["success"]:
        ...     print(f"Saved to: {result['output_path']}")
    """
    handler = DocumentHandler()

    # Handle file-like objects (FastAPI UploadFile)
    if hasattr(file, 'read'):
        file_content = file.read()
        if hasattr(file, 'seek'):
            file.seek(0)  # Reset file pointer
        if filename is None and hasattr(file, 'filename'):
            filename = file.filename
    else:
        file_content = file

    if filename is None:
        return {
            "success": False,
            "message": "Filename must be provided",
            "output_path": None
        }

    return handler.process_file(file_content, filename, domain, company)


# CLI for standalone usage
def main():
    """Command-line interface for document processing."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Document Handler - Extract text from PDF/DOCX/TXT files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a PDF file
  python pdf_handler.py --file document.pdf --domain ecommerce --company amazon

  # Process a DOCX file
  python pdf_handler.py --file manual.docx --domain telecom --company airtel

  # Process a TXT file
  python pdf_handler.py --file readme.txt --domain education --company smit
        """
    )

    parser.add_argument('--file', required=True, help='Path to input file (PDF/DOCX/TXT)')
    parser.add_argument('--domain', required=True, help='Domain category')
    parser.add_argument('--company', required=True, help='Company name')

    args = parser.parse_args()

    # Read file
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"✗ File not found: {args.file}")
        sys.exit(1)

    with open(file_path, 'rb') as f:
        file_content = f.read()

    # Process file
    result = handle_pdf(file_content, args.domain, args.company, file_path.name)

    # Display result
    if result["success"]:
        print(f"\n✓ {result['message']}")
        print(f"  Output: {result['output_path']}")
        print(f"  Characters: {result.get('characters_extracted', 'N/A')}")
    else:
        print(f"\n✗ {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
