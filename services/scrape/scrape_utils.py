import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import re

SCRAPE_PATH = "scraped_data/calligraphy_content.json"
MAX_AGE_SECONDS = 3 * 30 * 24 * 60 * 60  # ≈ 3 months

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0; +http://yourdomain.com/bot)"
}


def clean_text(text):
    # Remove unusual/control characters and multiple blank lines
    text = re.sub(r'[^\x20-\x7E\n\r\t]', ' ', text)  # keep printable ASCII and whitespace chars
    text = re.sub(r'\n\s*\n', '\n\n', text)  # collapse multiple blank lines
    text = re.sub(r'[ \t]+', ' ', text)  # normalize spaces/tabs
    return text.strip()

def text_to_markdown(text):
    # Simple markdown clean-up, can be enhanced
    # Escape markdown special chars or just preserve plain text
    # Here we just return cleaned plain text for simplicity
    return clean_text(text)

def is_recent_scrape():
    if not os.path.exists(SCRAPE_PATH):
        return False
    last_modified = os.path.getmtime(SCRAPE_PATH)
    return (time.time() - last_modified) < MAX_AGE_SECONDS

def normalize_url(base, link):
    # Join relative link with base URL and remove fragment
    full_url = urljoin(base, link)
    return urldefrag(full_url).url  # Removes the #fragment part

def scrape_calligraphy_cut(base_url="https://calligraphy-cut.com/"):
    visited = set()
    results = []

    print(f"🕷️ Fetching main page: {base_url}")
    try:
        res = requests.get(base_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"❌ Failed to fetch main page: {e}")
        return []

    # Always scrape main page content itself
    main_text = soup.get_text(separator="\n", strip=True)
    if len(main_text.strip()) > 100:
        md_content = text_to_markdown(main_text)
        results.append({"url": base_url, "content": md_content})
        visited.add(base_url)
        print(f"✅ Scraped main page (English): {base_url}")
    else:
        print(f"⚠️ Main page is not English or too short, skipping content.")

    # Collect internal links only from main page
    internal_links = set()
    base_domain = urlparse(base_url).netloc

    for link in soup.find_all("a", href=True):
        full_url = normalize_url(base_url, link["href"]).rstrip("/")
        if full_url.startswith("mailto:") or full_url.startswith("tel:"):
            continue
        if any(full_url.endswith(ext) for ext in [".jpg", ".png", ".pdf", ".svg", ".css", ".js"]):
            continue
        internal_links.add(full_url)

    print(f"🔗 Found {len(internal_links)} internal links on main page.")

    for url in internal_links:
        if url in visited:
            continue
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            if len(text.strip()) > 100:
                md_content = text_to_markdown(text)
                results.append({"url": url, "content": md_content})
                print(f"✅ Scraped (English): {url}")
            else:
                print(f"⚠️ Skipping non-English or too short page: {url}")
            visited.add(url)
        except Exception as e:
            print(f"⚠️  Failed to fetch {url}: {e}")

    print(f"\n💾 Saving {len(results)} pages to {SCRAPE_PATH}")
    os.makedirs(os.path.dirname(SCRAPE_PATH), exist_ok=True)
    with open(SCRAPE_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results


def get_or_scrape_data():
    if is_recent_scrape():
        print("✅ Using cached scraped data.")
        with open(SCRAPE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("🕷️ Scraping new data from calligraphy-cut.com ...")
        return scrape_calligraphy_cut()
