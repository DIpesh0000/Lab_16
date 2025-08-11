""" Refactor the textbook's hn_submissions.py so it doesn't crash on
         missing fields (like 'descendants'). Fetch top Hacker News stories,
         handle errors, and print a simple ranked list. 8/10/2025 BY:DIPESH DAHAL
"""

import time
import requests

TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
HN_LINK  = "https://news.ycombinator.com/item?id={id}"

def fetch_json(url, timeout=10):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"[warn] request failed: {url} -> {e}")
        return None
    except ValueError:
        print(f"[warn] bad json: {url}")
        return None

def main():
    print("Getting top Hacker News story IDs...")
    ids = fetch_json(TOP_URL)
    if not isinstance(ids, list) or not ids:
        print("Could not load top stories.")
        return

    limit = 30
    entries = []

    print(f"Fetching first {limit} items (skipping any broken ones)...")
    for i, sid in enumerate(ids[:limit], start=1):
        item = fetch_json(ITEM_URL.format(id=sid))
        if not isinstance(item, dict):
            print(f"[skip] id={sid} (no item)")
            continue

        title = item.get("title", "<no title>")
        by = item.get("by", "<unknown>")
        url = item.get("url") or HN_LINK.format(id=sid)

        try:
            score = int(item.get("score", 0))
        except (TypeError, ValueError):
            score = 0
        try:
            comments = int(item.get("descendants", 0))  
        except (TypeError, ValueError):
            comments = 0

        entries.append({
            "id": sid,
            "title": title,
            "by": by,
            "url": url,
            "hn": HN_LINK.format(id=sid),
            "score": score,
            "comments": comments
        })

        time.sleep(0.1)

    if not entries:
        print("No stories to show.")
        return

    
    entries.sort(key=lambda e: (e["comments"], e["score"]), reverse=True)

    print("\nTop Hacker News stories (safe version, no KeyError):\n")
    for idx, e in enumerate(entries, start=1):
        print(f"{idx}. {e['title']}")
        print(f"   by: {e['by']} | comments: {e['comments']} | score: {e['score']}")
        print(f"   url: {e['url']}")
        print(f"   hn:  {e['hn']}\n")

if __name__ == "__main__":
    main()