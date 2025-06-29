import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .utils import normalize_url, is_recent_scrape, clean_text
from .conifg import SCRAPE_PATH, HEADERS, base_url

def scrape_calligraphy_cut(base_url=base_url):
    """
    Scrape text content from the main page and internal pages of the given base URL.

    - Extracts and cleans English text from the base page.
    - Identifies internal links (excluding media and non-HTML files).
    - Scrapes and cleans text from each internal link if it has meaningful content.
    - Saves the results to SCRAPE_PATH in JSON format.

    Args:
        base_url (str): The URL of the website to scrape (defaults to configured `base_url`).

    Returns:
        List[Dict]: A list of dictionaries containing 'url' and 'content' for each successfully scraped page.
    """

    visited = set()
    results = []

    print(f"Fetching main page: {base_url}")
    try:
        res = requests.get(base_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"Failed to fetch main page: {e}")
        return []

    # Always scrape main page content itself
    main_text = soup.get_text(separator="\n", strip=True)
    if len(main_text.strip()) > 100:
        md_content = (main_text)
        results.append({"url": base_url, "content": md_content})
        visited.add(base_url)
        print(f"Scraped main page (English): {base_url}")
    else:
        print(f"Main page is not English or too short, skipping content.")

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

    print(f"Found {len(internal_links)} internal links on main page.")

    for url in internal_links:
        if url in visited:
            continue
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            if len(text.strip()) > 100:
                md_content = clean_text(text)
                results.append({"url": url, "content": md_content})
                print(f"Scraped (English): {url}")
            else:
                print(f"Skipping non-English or too short page: {url}")
            visited.add(url)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    print(f"\n Saving {len(results)} pages to {SCRAPE_PATH}")
    os.makedirs(os.path.dirname(SCRAPE_PATH), exist_ok=True)
    with open(SCRAPE_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results

def get_or_scrape_data():
    """
    Return cached scrape results if they are recent enough.
    Otherwise, scrape new data from the target site.

    Returns:
        List[Dict]: List of scraped page data (from cache or fresh scrape).
    """
    if is_recent_scrape():
        print("Using cached scraped data.")
        with open(SCRAPE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("Scraping new data from calligraphy-cut.com ...")
        return scrape_calligraphy_cut()
