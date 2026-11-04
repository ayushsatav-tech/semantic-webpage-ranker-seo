
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


def analyze_webpage(url):
    # Check URL format
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ["http", "https"] or not parsed_url.netloc:
        raise ValueError("Enter a valid webpage URL starting with http:// or https://")

    # Download webpage
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; SEOAnalyzer/1.0)"},
        timeout=15
    )
    response.raise_for_status()

    # Extract webpage content
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.get_text(strip=True) if soup.title else ""

    meta_tag = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    meta_description = meta_tag.get("content", "").strip() if meta_tag else ""

    headings = {
        "H1": [tag.get_text(" ", strip=True) for tag in soup.find_all("h1")],
        "H2": [tag.get_text(" ", strip=True) for tag in soup.find_all("h2")]
    }

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)
    words = re.findall(r"\b[a-zA-Z0-9]+\b", text)

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "word_count": len(words),
        "content": text
    }
