"""
Enhanced PDF Handler - Saves Original + Extracted Text
For easy WebUI integration with original file preservation
"""

import sys
from pathlib import Path
from typing import Dict, Union, BinaryIO

# Set UTF-8 for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import the existing pdf_handler
from pdf_handler import handle_pdf as extract_text


def handle_pdf_with_original(
    file: Union[bytes, BinaryIO],
    domain: str,
    company: str,
    filename: str,
    base_dir: str = "."
) -> Dict:
    """
    Enhanced handler that:
    1. Saves original PDF/DOCX to policies/{domain}/{company}/
    2. Extracts text to raw_data/{domain}/{company}/

    Perfect for WebUI integration!

    Args:
        file: File content (bytes or file-like object)
        domain: Domain category
        company: Company name
        filename: Original filename with extension
        base_dir: Base directory (default: current)

    Returns:
        Dict with both original and extracted paths
    """
    base_path = Path(base_dir)

    # Read file content if it's a file-like object
    if hasattr(file, 'read'):
        file_content = file.read()
        if hasattr(file, 'seek'):
            file.seek(0)
    else:
        file_content = file

    # === STEP 1: Save original file ===
    policies_dir = base_path / "policies" / domain / company
    policies_dir.mkdir(parents=True, exist_ok=True)

    original_path = policies_dir / filename

    try:
        with open(original_path, 'wb') as f:
            f.write(file_content)
        print(f"✓ Original saved: {original_path}")
        original_saved = True
    except Exception as e:
        print(f"✗ Failed to save original: {e}")
        original_saved = False

    # === STEP 2: Extract text ===
    extract_result = extract_text(
        file=file_content,
        domain=domain,
        company=company,
        filename=filename
    )

    # === STEP 3: Return combined result ===
    return {
        "success": extract_result["success"] and original_saved,
        "message": extract_result["message"],
        "original_path": str(original_path.relative_to(base_path)) if original_saved else None,
        "extracted_path": extract_result.get("output_path"),
        "characters_extracted": extract_result.get("characters_extracted"),
        "domain": domain,
        "company": company,
        "filename": filename
    }


def list_pdfs(domain: str, company: str, base_dir: str = ".") -> Dict:
    """
    List all original PDFs for a company.

    Returns:
        Dict with list of PDF info (filename, size, modified date)
    """
    policies_dir = Path(base_dir) / "policies" / domain / company

    if not policies_dir.exists():
        return {
            "domain": domain,
            "company": company,
            "count": 0,
            "files": []
        }

    files = []
    for pdf_file in sorted(policies_dir.glob("*.*")):
        if pdf_file.is_file():
            stat = pdf_file.stat()
            files.append({
                "filename": pdf_file.name,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / 1024 / 1024, 2),
                "modified": stat.st_mtime,
                "extension": pdf_file.suffix
            })

    return {
        "domain": domain,
        "company": company,
        "count": len(files),
        "files": files
    }


def get_original_path(domain: str, company: str, filename: str, base_dir: str = ".") -> Path:
    """
    Get path to original PDF file.

    Returns:
        Path object to the original file
    """
    return Path(base_dir) / "policies" / domain / company / filename


# CLI for testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Upload and process documents')
    parser.add_argument('--file', required=True, help='Path to file')
    parser.add_argument('--domain', required=True, help='Domain category')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--list', action='store_true', help='List existing PDFs')

    args = parser.parse_args()

    if args.list:
        # List PDFs
        result = list_pdfs(args.domain, args.company)
        print(f"\n📁 PDFs for {args.domain}/{args.company}:")
        print(f"Total files: {result['count']}\n")

        for file_info in result['files']:
            print(f"  {file_info['filename']}")
            print(f"    Size: {file_info['size_mb']} MB")
            print(f"    Type: {file_info['extension']}")
            print()
    else:
        # Upload and process
        file_path = Path(args.file)

        if not file_path.exists():
            print(f"✗ File not found: {args.file}")
            sys.exit(1)

        with open(file_path, 'rb') as f:
            result = handle_pdf_with_original(
                file=f,
                domain=args.domain,
                company=args.company,
                filename=file_path.name
            )

        if result['success']:
            print(f"\n✓ Successfully processed {args.file}")
            print(f"\n📄 Original PDF:")
            print(f"   {result['original_path']}")
            print(f"\n📝 Extracted Text:")
            print(f"   {result['extracted_path']}")
            print(f"   Characters: {result['characters_extracted']}")
        else:
            print(f"\n✗ Processing failed: {result['message']}")
            sys.exit(1)
