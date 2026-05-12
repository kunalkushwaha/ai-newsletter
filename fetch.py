#!/usr/bin/env python3
"""
Fetches raw content from all configured AI news sources.
Outputs a JSON file: raw_content.json
The summarization is handled by the calling Claude Code agent.
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

CONFIG_PATH = Path(__file__).parent / "config.json"
OUTPUT_PATH = Path(__file__).parent / "raw_content.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AI-Newsletter-Bot/1.0)"}
FETCH_TIMEOUT = 15


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def is_rss(url):
    return any(x in url for x in ["rss", "feed", "atom", "hnrss.org"])


def parse_rss_date(date_str):
    if not date_str:
        return None
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
    ):
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def fetch_rss(url, max_days):
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [warn] {url}: {e}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f"  [warn] XML parse error {url}: {e}", file=sys.stderr)
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = []

    # Atom feeds
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title_el = entry.find("{http://www.w3.org/2005/Atom}title")
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        published_el = entry.find("{http://www.w3.org/2005/Atom}published") or entry.find("{http://www.w3.org/2005/Atom}updated")
        summary_el = entry.find("{http://www.w3.org/2005/Atom}summary") or entry.find("{http://www.w3.org/2005/Atom}content")

        title = title_el.text if title_el is not None else ""
        link = link_el.get("href", "") if link_el is not None else ""
        date_str = published_el.text if published_el is not None else ""
        summary = summary_el.text if summary_el is not None else ""

        published = parse_rss_date(date_str)
        if published and published < cutoff:
            continue
        text = BeautifulSoup(summary or "", "html.parser").get_text(separator=" ", strip=True)[:500]
        items.append({
            "title": title,
            "url": link,
            "date": published.isoformat() if published else "unknown",
            "snippet": text,
        })

    # RSS 2.0 feeds
    if not items:
        for item in root.iter("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pubdate_el = item.find("pubDate")
            desc_el = item.find("description")

            title = title_el.text if title_el is not None else ""
            link = link_el.text if link_el is not None else ""
            date_str = pubdate_el.text if pubdate_el is not None else ""
            summary = desc_el.text if desc_el is not None else ""

            published = parse_rss_date(date_str)
            if published and published < cutoff:
                continue
            text = BeautifulSoup(summary or "", "html.parser").get_text(separator=" ", strip=True)[:500]
            items.append({
                "title": title,
                "url": link,
                "date": published.isoformat() if published else "unknown",
                "snippet": text,
            })

    return items


def fetch_html(url, max_days):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [warn] {url}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    items = []
    seen = set()
    for tag in soup.find_all(["article", "h1", "h2", "h3"]):
        link = tag.find("a", href=True)
        if not link:
            continue
        title = link.get_text(strip=True)
        href = link["href"]
        if not title or href in seen or len(title) < 10:
            continue
        seen.add(href)
        if href.startswith("/"):
            from urllib.parse import urlparse
            base = urlparse(url)
            href = f"{base.scheme}://{base.netloc}{href}"
        snippet = tag.get_text(separator=" ", strip=True)[:300]
        items.append({"title": title, "url": href, "date": "recent", "snippet": snippet})

    if not items:
        text = soup.get_text(separator="\n", strip=True)
        lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 40]
        return [{"title": url, "url": url, "date": "recent", "snippet": "\n".join(lines[:60])}]

    return items[:20]


def main():
    print("=== Fetching AI News Sources ===", file=sys.stderr)
    config = load_config()
    max_days = config["filters"]["max_days_old"]
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sources = sorted(config["sources"], key=lambda s: priority_order.get(s["priority"], 3))

    all_items = []
    for source in sources:
        print(f"  [{source['priority']}] {source['name']} ...", file=sys.stderr)
        try:
            items = fetch_rss(source["url"], max_days) if is_rss(source["url"]) else fetch_html(source["url"], max_days)
            for item in items:
                item["source"] = source["name"]
                item["priority"] = source["priority"]
            all_items.extend(items)
            print(f"    -> {len(items)} items", file=sys.stderr)
        except Exception as e:
            print(f"    -> error: {e}", file=sys.stderr)

    result = {
        "fetched_at": datetime.now().isoformat(),
        "total_items": len(all_items),
        "config": {
            "intent": config["intent"],
            "tone": config["output"]["tone"],
            "sections": config["output"]["sections"],
            "max_items_per_section": config["output"]["max_items_per_section"],
            "boost_topics": config["filters"]["boost_topics"],
            "skip_topics": config["filters"]["skip_topics"],
        },
        "items": all_items,
    }

    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(all_items)} items to {OUTPUT_PATH}", file=sys.stderr)
    print(f"FETCH_COMPLETE:{len(all_items)}")


if __name__ == "__main__":
    main()
