from .conifg import SCRAPE_PATH, MAX_AGE_SECONDS
from urllib.parse import urljoin, urldefrag
import os

import time
import re

def clean_text(text):
    """
    Clean the given text by:
    - Removing non-printable/control characters
    - Collapsing multiple blank lines
    - Normalizing spaces and tabs

    Args:
        text (str): The raw text to be cleaned.

    Returns:
        str: The cleaned and normalized text.
    """

    text = re.sub(r'[^\x20-\x7E\n\r\t]', ' ', text)  
    text = re.sub(r'\n\s*\n', '\n\n', text)  
    text = re.sub(r'[ \t]+', ' ', text)  
    return text.strip()

def is_recent_scrape():
    
    """
    Check if the scrape file exists and is still considered recent.

    Returns:
        bool: True if the file at SCRAPE_PATH was modified within MAX_AGE_SECONDS, else False.
    """

    if not os.path.exists(SCRAPE_PATH):
        return False
    last_modified = os.path.getmtime(SCRAPE_PATH)
    return (time.time() - last_modified) < MAX_AGE_SECONDS

def normalize_url(base, link):
    """
    Normalize a URL by resolving it against a base URL and removing any fragment.

    Args:
        base (str): The base URL.
        link (str): A possibly relative or fragment-containing URL.

    Returns:
        str: A fully-qualified, fragment-free URL.
    """

    full_url = urljoin(base, link)
    return urldefrag(full_url).url  
