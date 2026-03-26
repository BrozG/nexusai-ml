"""
Universal Web Fetcher and Content Tracker
Scrapes URLs, tracks content changes, and manages domain-specific raw data.
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False

try:
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fetcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class UniversalFetcher:
    """Handles web scraping, content tracking, and automatic updates."""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.raw_data_dir = self.base_dir / "raw_data"
        self.vector_stores_dir = self.base_dir / "vector_stores"

    def _ensure_directories(self, domain: str, company: str) -> Tuple[Path, Path]:
        """Create necessary directory structure."""
        raw_path = self.raw_data_dir / domain / company
        tracker_path = self.vector_stores_dir / domain / company

        raw_path.mkdir(parents=True, exist_ok=True)
        tracker_path.mkdir(parents=True, exist_ok=True)

        return raw_path, tracker_path

    def _get_page_name(self, url: str) -> str:
        """Extract a clean page name from URL."""
        parsed = urlparse(url)
        path = parsed.path.strip('/').replace('/', '_')

        if not path:
            path = parsed.netloc.replace('.', '_')

        # Clean the name
        path = re.sub(r'[^\w\-_]', '_', path)
        path = re.sub(r'_+', '_', path)
        path = path[:100]  # Limit length

        return path if path else 'index'

    def _fetch_and_clean(self, url: str) -> Optional[str]:
        """Fetch URL and extract clean text content."""
        if not SCRAPING_AVAILABLE:
            logger.error("Scraping dependencies not installed. Run: pip install requests beautifulsoup4 lxml")
            return None

        try:
            logger.info(f"Fetching: {url}")

            # More complete headers to appear like a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            # Add retry logic with exponential backoff
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed, retrying... ({e})")
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()

            # Extract text
            text = soup.get_text(separator='\n', strip=True)

            # Clean whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            cleaned_text = '\n'.join(lines)

            # Remove excessive newlines
            cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

            logger.info(f"Successfully fetched {len(cleaned_text)} characters from {url}")
            return cleaned_text

        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            return None

    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _load_tracker(self, tracker_path: Path) -> Dict:
        """Load URL tracker JSON."""
        tracker_file = tracker_path / "url_tracker.json"

        if tracker_file.exists():
            with open(tracker_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"urls": []}

    def _save_tracker(self, tracker_path: Path, tracker_data: Dict):
        """Save URL tracker JSON."""
        tracker_file = tracker_path / "url_tracker.json"

        with open(tracker_file, 'w', encoding='utf-8') as f:
            json.dump(tracker_data, f, indent=2, ensure_ascii=False)

    def fetch_url(self, domain: str, company: str, url: str) -> bool:
        """
        Fetch a single URL and save to appropriate locations.

        Args:
            domain: Domain category (e.g., 'ecommerce', 'education', 'telecom')
            company: Company name
            url: URL to fetch

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directories exist
            raw_path, tracker_path = self._ensure_directories(domain, company)

            # Fetch and clean content
            content = self._fetch_and_clean(url)
            if not content:
                return False

            # Compute hash
            content_hash = self._compute_hash(content)
            page_name = self._get_page_name(url)
            timestamp = datetime.now().isoformat()

            # Save raw text
            raw_file = raw_path / f"url_{page_name}.txt"
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved to: {raw_file}")

            # Update tracker
            tracker_data = self._load_tracker(tracker_path)

            # Find or create entry
            url_entry = None
            for entry in tracker_data["urls"]:
                if entry["url"] == url:
                    url_entry = entry
                    break

            if url_entry:
                # Update existing entry
                url_entry["hash"] = content_hash
                url_entry["last_updated"] = timestamp
                url_entry["file_path"] = str(raw_file.relative_to(self.base_dir))
            else:
                # Add new entry
                tracker_data["urls"].append({
                    "url": url,
                    "hash": content_hash,
                    "last_updated": timestamp,
                    "file_path": str(raw_file.relative_to(self.base_dir)),
                    "page_name": page_name
                })

            self._save_tracker(tracker_path, tracker_data)
            logger.info(f"Updated tracker for {domain}/{company}")

            return True

        except Exception as e:
            logger.error(f"Error in fetch_url: {e}")
            return False

    def check_updates(self) -> Dict[str, int]:
        """
        Check all tracked URLs for updates across all domains and companies.

        Returns:
            Statistics dict with counts
        """
        stats = {
            "total_checked": 0,
            "updated": 0,
            "unchanged": 0,
            "failed": 0
        }

        logger.info("Starting update check for all tracked URLs...")

        # Iterate through all vector_stores directories
        if not self.vector_stores_dir.exists():
            logger.warning(f"Vector stores directory not found: {self.vector_stores_dir}")
            return stats

        for domain_dir in self.vector_stores_dir.iterdir():
            if not domain_dir.is_dir():
                continue

            domain = domain_dir.name

            for company_dir in domain_dir.iterdir():
                if not company_dir.is_dir():
                    continue

                company = company_dir.name
                tracker_file = company_dir / "url_tracker.json"

                if not tracker_file.exists():
                    continue

                logger.info(f"Checking {domain}/{company}...")
                tracker_data = self._load_tracker(company_dir)

                for entry in tracker_data["urls"]:
                    stats["total_checked"] += 1
                    url = entry["url"]
                    old_hash = entry.get("hash", "")

                    # Fetch current content
                    content = self._fetch_and_clean(url)

                    if not content:
                        stats["failed"] += 1
                        logger.warning(f"Failed to fetch: {url}")
                        continue

                    # Check if content changed
                    new_hash = self._compute_hash(content)

                    if new_hash != old_hash:
                        stats["updated"] += 1
                        logger.info(f"Content changed: {url}")

                        # Update file
                        raw_path = self.base_dir / entry["file_path"]
                        raw_path.parent.mkdir(parents=True, exist_ok=True)

                        with open(raw_path, 'w', encoding='utf-8') as f:
                            f.write(content)

                        # Update tracker entry
                        entry["hash"] = new_hash
                        entry["last_updated"] = datetime.now().isoformat()

                    else:
                        stats["unchanged"] += 1

                # Save updated tracker
                self._save_tracker(company_dir, tracker_data)

        logger.info(f"Update check complete: {stats}")
        return stats

    def get_all_tracked_urls(self) -> List[Dict]:
        """Get list of all tracked URLs across all domains."""
        all_urls = []

        if not self.vector_stores_dir.exists():
            return all_urls

        for domain_dir in self.vector_stores_dir.iterdir():
            if not domain_dir.is_dir():
                continue

            for company_dir in domain_dir.iterdir():
                if not company_dir.is_dir():
                    continue

                tracker_file = company_dir / "url_tracker.json"
                if tracker_file.exists():
                    tracker_data = self._load_tracker(company_dir)

                    for entry in tracker_data["urls"]:
                        all_urls.append({
                            "domain": domain_dir.name,
                            "company": company_dir.name,
                            **entry
                        })

        return all_urls


def run_scheduler():
    """Run the scheduler for nightly updates."""
    if not SCHEDULER_AVAILABLE:
        logger.error("APScheduler not installed. Run: pip install APScheduler")
        print("\n✗ Scheduler requires APScheduler. Install with:")
        print("  pip install APScheduler")
        sys.exit(1)

    fetcher = UniversalFetcher()
    scheduler = BlockingScheduler()

    # Schedule nightly updates at 2 AM
    scheduler.add_job(
        fetcher.check_updates,
        trigger=CronTrigger(hour=2, minute=0),
        id='nightly_update',
        name='Check URL updates nightly',
        replace_existing=True
    )

    logger.info("Scheduler started. Updates will run daily at 2:00 AM")
    logger.info("Press Ctrl+C to exit")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Universal Web Fetcher - Scrape and track web content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch a single URL
  python universal_fetcher.py --domain ecommerce --company amazon --input https://example.com/faq

  # Check all tracked URLs for updates
  python universal_fetcher.py --check-updates

  # Start scheduler for nightly updates
  python universal_fetcher.py --scheduler

  # List all tracked URLs
  python universal_fetcher.py --list
        """
    )

    parser.add_argument('--domain', type=str, help='Domain category (e.g., ecommerce, education, telecom)')
    parser.add_argument('--company', type=str, help='Company name')
    parser.add_argument('--input', type=str, help='URL to fetch')
    parser.add_argument('--check-updates', action='store_true', help='Check all tracked URLs for updates')
    parser.add_argument('--scheduler', action='store_true', help='Start nightly update scheduler')
    parser.add_argument('--list', action='store_true', help='List all tracked URLs')

    args = parser.parse_args()

    fetcher = UniversalFetcher()

    # Handle different modes
    if args.scheduler:
        run_scheduler()

    elif args.check_updates:
        stats = fetcher.check_updates()
        print("\n" + "="*50)
        print("UPDATE CHECK SUMMARY")
        print("="*50)
        print(f"Total URLs checked: {stats['total_checked']}")
        print(f"Content updated:    {stats['updated']}")
        print(f"Unchanged:          {stats['unchanged']}")
        print(f"Failed:             {stats['failed']}")
        print("="*50)

    elif args.list:
        urls = fetcher.get_all_tracked_urls()
        print(f"\nTracked URLs: {len(urls)}\n")

        for url_data in urls:
            print(f"{url_data['domain']}/{url_data['company']}")
            print(f"  URL: {url_data['url']}")
            print(f"  Last Updated: {url_data.get('last_updated', 'N/A')}")
            print(f"  File: {url_data.get('file_path', 'N/A')}")
            print()

    elif args.domain and args.company and args.input:
        success = fetcher.fetch_url(args.domain, args.company, args.input)

        if success:
            print(f"\n✓ Successfully fetched and saved content from {args.input}")
        else:
            print(f"\n✗ Failed to fetch content from {args.input}")
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
