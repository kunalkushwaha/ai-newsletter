#!/usr/bin/env python3
"""
Weekly AI Newsletter Generator
Fetches content from configured sources, summarizes via Claude API, commits to git.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import anthropic
import feedparser
import requests
from bs4 import BeautifulSoup

CONFIG_PATH = Path(__file__).parent / "config.json"
OUTPUT_DIR = Path(__file__).parent / "newsletters"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AI-Newsletter-Bot/1.0)"
}
FETCH_TIMEOUT = 15


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def is_rss(url):
    return any(x in url for x in ["rss", "feed", "atom", "hnrss.org"])


def fetch_rss(url, max_days):
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        published = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        summary = entry.get("summary", "")
        soup = BeautifulSoup(summary, "html.parser")
        text = soup.get_text(separator=" ", strip=True)[:500]
        if published and published < cutoff:
            continue
        items.append({
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "date": published.isoformat() if published else "unknown",
            "snippet": text,
        })
    return items


def fetch_html(url, max_days):
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [warn] Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Extract candidate article links with titles
    items = []
    seen = set()
    for tag in soup.find_all(["article", "h2", "h3", "h1"]):
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

    # Fallback: grab all visible text if no articles found
    if not items:
        text = soup.get_text(separator="\n", strip=True)
        lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 40]
        return [{"title": url, "url": url, "date": "recent", "snippet": "\n".join(lines[:60])}]

    return items[:20]


def fetch_all_sources(config):
    max_days = config["filters"]["max_days_old"]
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sources = sorted(config["sources"], key=lambda s: priority_order.get(s["priority"], 3))

    all_content = []
    for source in sources:
        print(f"  Fetching [{source['priority']}] {source['name']} ...")
        try:
            if is_rss(source["url"]):
                items = fetch_rss(source["url"], max_days)
            else:
                items = fetch_html(source["url"], max_days)
            for item in items:
                item["source"] = source["name"]
                item["priority"] = source["priority"]
            all_content.extend(items)
            print(f"    -> {len(items)} items")
        except Exception as e:
            print(f"    -> error: {e}")

    return all_content


def build_prompt(config, content):
    today = datetime.now().strftime("%Y-%m-%d")
    sections = "\n".join(f"- {s}" for s in config["output"]["sections"])
    boost = ", ".join(config["filters"]["boost_topics"])
    skip = ", ".join(config["filters"]["skip_topics"])

    # Serialize fetched content compactly
    content_text = ""
    for item in content:
        content_text += f"[{item['source']}] {item['title']}\n  {item['snippet']}\n  URL: {item['url']}\n\n"

    return f"""Today is {today}. You are writing a weekly AI newsletter.

INTENT: {config['intent']}

TONE: {config['output']['tone']}

SECTIONS TO INCLUDE (in this order):
{sections}

BOOST these topics (elevate to higher sections): {boost}
SKIP these topics entirely: {skip}

RAW CONTENT FETCHED FROM SOURCES (last 7 days):
---
{content_text[:80000]}
---

Instructions:
- Only include items clearly published in the past 7 days. Discard anything older or undated that seems stale.
- Deduplicate: if the same story appears from multiple sources, merge into one entry.
- Write the newsletter in markdown. Start with:

# AI Newsletter — Week of {today}

Then a 2-sentence intro summarizing the week's theme.

Then each section. Max {config['output']['max_items_per_section']} items per section.
Top Stories: 2-3 sentences per item. Quick Links: one line each.

End with:
---
*Generated by Claude Code on {today}. Sources used: [list sources that contributed content]*

Be concise. No filler. No hype."""


def generate_newsletter(config, content):
    client = anthropic.Anthropic()
    prompt = build_prompt(config, content)

    print("  Calling Claude API...")
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def save_newsletter(text):
    OUTPUT_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"newsletter-{today}.md"
    output_file.write_text(text, encoding="utf-8")
    print(f"  Saved: {output_file}")

    # Update index
    index_file = OUTPUT_DIR / "index.md"
    # Extract first non-header, non-blank line as theme
    theme = next(
        (l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")),
        "Weekly AI news roundup"
    )
    entry = f"- [Newsletter {today}](newsletter-{today}.md) — {theme[:120]}\n"
    with open(index_file, "a", encoding="utf-8") as f:
        f.write(entry)

    return output_file


def git_push(output_file):
    repo_dir = Path(__file__).parent
    today = datetime.now().strftime("%Y-%m-%d")
    cmds = [
        ["git", "-C", str(repo_dir), "config", "user.email", "claude-code@anthropic.com"],
        ["git", "-C", str(repo_dir), "config", "user.name", "Claude Code"],
        ["git", "-C", str(repo_dir), "add", "newsletters/"],
        ["git", "-C", str(repo_dir), "commit", "-m", f"Newsletter: Week of {today}"],
        ["git", "-C", str(repo_dir), "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  [git error] {' '.join(cmd[3:])}: {result.stderr.strip()}")
            return False
    print("  Pushed to GitHub.")
    return True


def main():
    print("=== Weekly AI Newsletter Generator ===")

    print("\n[1/4] Loading config...")
    config = load_config()

    print("\n[2/4] Fetching sources...")
    content = fetch_all_sources(config)
    print(f"  Total items collected: {len(content)}")

    if not content:
        print("No content fetched. Exiting.")
        sys.exit(1)

    print("\n[3/4] Generating newsletter with Claude...")
    newsletter_text = generate_newsletter(config, content)

    print("\n[4/4] Saving and pushing...")
    output_file = save_newsletter(newsletter_text)
    git_push(output_file)

    print("\n=== Done ===")
    print(newsletter_text)


if __name__ == "__main__":
    main()
