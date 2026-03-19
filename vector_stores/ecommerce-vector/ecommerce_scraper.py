"""
ecommerce_scraper.py  (v2 — improved)
======================================
Scrapes e-commerce help center pages and builds the source document corpus.

Improvements over v1
--------------------
* Loads from the comprehensive 68-article built-in knowledge base
  (knowledge_base.py) covering 12 topics with 400–600 word articles
* Incorporates the 1000-record customer interaction dataset as supplementary
  context passages that add real-world query phrasing to the corpus
* Live scraper targets more sub-pages per help center, filters for minimum
  200-character paragraphs, and preserves heading structure
* Deduplication using MD5 hash of normalised text prefixes
* Modular output format: {source, topic, title, text}

Pipeline:
    Knowledge Base + Dataset + Live Scraping
    → Deduplication + Quality Filtering
    → scraped_support_text.json

Usage:
    python ecommerce_scraper.py
"""

import json
import logging
import re
import time
import hashlib
import os
from dataclasses import dataclass, asdict
from typing import Optional
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
REQUEST_TIMEOUT = 15
CRAWL_DELAY     = 1.5
MIN_PARA_LEN    = 200   # chars

HELP_PAGES = {
    "amazon_refunds":         "https://www.amazon.in/gp/help/customer/display.html?nodeId=201819150",
    "amazon_returns":         "https://www.amazon.in/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7",
    "amazon_cancel":          "https://www.amazon.in/gp/help/customer/display.html?nodeId=201929620",
    "amazon_payments":        "https://www.amazon.in/gp/help/customer/display.html?nodeId=202140860",
    "amazon_damaged":         "https://www.amazon.in/gp/help/customer/display.html?nodeId=G4YFYCCNUSENA23P",
    "amazon_delivery_issues": "https://www.amazon.in/gp/help/customer/display.html?nodeId=G202124970",
    "amazon_account":         "https://www.amazon.in/gp/help/customer/display.html?nodeId=G69129",
    "amazon_prime":           "https://www.amazon.in/gp/help/customer/display.html?nodeId=G34EUPKVMYFW8N2U",
    "flipkart_returns":       "https://www.flipkart.com/pages/returnpolicy",
    "flipkart_payments":      "https://www.flipkart.com/pages/paymentshelp",
    "ebay_money_back":        "https://www.ebay.com/help/buying/returns-refunds/ebay-money-back-guarantee?id=4190",
    "ebay_returns":           "https://www.ebay.com/help/buying/returns-refunds/return-item-refund?id=4041",
    "ebay_payment":           "https://www.ebay.com/help/buying/paying-items/paying-items?id=4019",
    "ebay_not_received":      "https://www.ebay.com/help/buying/returns-refunds/missing-items?id=4042",
}

NOISE_TAGS = {"script","style","nav","header","footer","aside",
              "noscript","form","button","iframe","meta","link","svg","img"}

TOPIC_KW_MAP = {
    "refund":    "refund_policy",
    "return":    "return_policy",
    "cancel":    "order_cancellation",
    "deliver":   "delivery_issues",
    "missing":   "delivery_issues",
    "shipment":  "tracking_shipping",
    "track":     "tracking_shipping",
    "payment":   "payment_failures",
    "charge":    "payment_failures",
    "damage":    "damaged_items",
    "defect":    "damaged_items",
    "broken":    "damaged_items",
    "replace":   "product_replacement",
    "account":   "account_issues",
    "login":     "account_issues",
    "password":  "account_issues",
    "warranty":  "warranty_service",
    "seller":    "seller_disputes",
}


@dataclass
class SupportDocument:
    source: str
    topic:  str
    title:  str
    text:   str


def _hash(text: str) -> str:
    normalised = re.sub(r"\s+", " ", text.lower().strip())[:500]
    return hashlib.md5(normalised.encode()).hexdigest()


def _classify_topic(text: str) -> str:
    lower = text.lower()
    for kw, topic in TOPIC_KW_MAP.items():
        if kw in lower:
            return topic
    return "general_tips"


# ── Live scraping ──────────────────────────────────────────────────────────
def fetch_page(url: str) -> Optional[str]:
    try:
        log.info("  Fetching: %s", url)
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        log.warning("  ✗ %s — %s", url, e)
        return None


def extract_clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(NOISE_TAGS):
        tag.decompose()
    paragraphs, seen = [], set()
    for elem in soup.find_all(["p","li","h1","h2","h3","h4","td","div","article"]):
        raw   = elem.get_text(separator=" ", strip=True)
        clean = re.sub(r"\s+", " ", raw).strip()
        if len(clean) >= MIN_PARA_LEN and clean[:120] not in seen:
            seen.add(clean[:120])
            paragraphs.append(clean)
    return "\n\n".join(paragraphs)


def scrape_live() -> list[SupportDocument]:
    docs = []
    for topic, url in HELP_PAGES.items():
        html = fetch_page(url)
        if html:
            text = extract_clean_text(html)
            if len(text.split()) >= 200:
                docs.append(SupportDocument(
                    source=url, topic=topic,
                    title=f"Live: {topic.replace('_',' ').title()}",
                    text=text,
                ))
                log.info("  ✓ %-30s %d words", topic, len(text.split()))
        time.sleep(CRAWL_DELAY)
    return docs


# ── Built-in knowledge base ────────────────────────────────────────────────
def load_knowledge_base() -> list[SupportDocument]:
    try:
        from knowledge_base import get_all_articles
        articles = get_all_articles()
        docs = [
            SupportDocument(
                source=a["source"], topic=a["topic"],
                title=a.get("title", a["source"]), text=a["text"],
            )
            for a in articles
        ]
        log.info("Loaded %d articles from knowledge_base.py", len(docs))
        return docs
    except ImportError:
        log.warning("knowledge_base.py not found")
        return []


# ── Customer interaction dataset ───────────────────────────────────────────
def load_interaction_dataset(path: str) -> list[SupportDocument]:
    """
    Convert 1000-record instruction→output dataset into grouped knowledge passages.
    Similar instructions are clustered and combined into coherent support articles.
    """
    if not os.path.exists(path):
        log.info("Dataset not found at %s — skipping", path)
        return []

    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    # Cluster by instruction stem (first 60 chars)
    clusters: dict[str, list[dict]] = defaultdict(list)
    for item in data:
        clusters[item["instruction"][:60]].append(item)

    docs, seen = [], set()
    for instruction, group in clusters.items():
        topic = _classify_topic(instruction)
        # Deduplicate outputs within cluster
        unique_outputs = list({d["output"][:200]: d["output"] for d in group}.values())

        passage = (
            f"Support Topic: {instruction}\n\n"
            + "\n\n".join(
                f"Agent Response: {o}" for o in unique_outputs[:5]
            )
        )

        if len(passage.split()) < 50:
            continue
        h = _hash(passage)
        if h in seen:
            continue
        seen.add(h)

        docs.append(SupportDocument(
            source=f"dataset/{topic}/{instruction[:40].replace(' ','_')}",
            topic=topic, title=instruction, text=passage,
        ))

    log.info("Converted dataset → %d support documents", len(docs))
    return docs


# ── Deduplication ──────────────────────────────────────────────────────────
def deduplicate(docs: list[SupportDocument]) -> list[SupportDocument]:
    seen, unique = set(), []
    for doc in docs:
        h = _hash(doc.text)
        if h not in seen:
            seen.add(h)
            unique.append(doc)
    log.info("After dedup: %d documents (removed %d)",
             len(unique), len(docs) - len(unique))
    return unique


# ── Public API ─────────────────────────────────────────────────────────────
def get_support_documents(
    try_live: bool = True,
    dataset_path: str = "/mnt/user-data/uploads/ecommerce_dataset_fixed_1000__1___1_.json",
) -> list[SupportDocument]:

    docs: list[SupportDocument] = []
    docs.extend(load_knowledge_base())
    docs.extend(load_interaction_dataset(dataset_path))

    if try_live:
        log.info("Attempting live scraping (%d URLs) …", len(HELP_PAGES))
        live = scrape_live()
        if live:
            log.info("Live scraping yielded %d documents", len(live))
            docs.extend(live)
        else:
            log.info("Live scraping unavailable — using offline corpus")

    docs = deduplicate(docs)
    log.info("Total source documents: %d", len(docs))
    return docs


def save_documents(docs: list[SupportDocument],
                   path: str = "scraped_support_text.json") -> None:
    payload = [asdict(d) for d in docs]
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    log.info("Saved %d documents → %s", len(docs), path)


# ── CLI ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from collections import Counter
    documents = get_support_documents(try_live=True)
    save_documents(documents, "scraped_support_text.json")

    topics = Counter(d.topic for d in documents)
    print(f"\n✅  Done — {len(documents)} source documents")
    for topic, count in sorted(topics.items()):
        print(f"  {topic:35s} {count}")
