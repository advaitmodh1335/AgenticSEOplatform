import requests
from bs4 import BeautifulSoup


def scrape_url(url: str):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = (
        meta_tag.get("content", "").strip()
        if meta_tag
        else "No meta description found"
    )

    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text:
            headings.append(text)

    paragraphs = []
    for tag in soup.find_all("p"):
        text = tag.get_text(strip=True)
        if text:
            paragraphs.append(text)

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings[:20],
        "content_preview": paragraphs[:10],
    }