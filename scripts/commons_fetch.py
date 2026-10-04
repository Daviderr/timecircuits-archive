"""Download freely licensed images from Wikimedia Commons with their credits.

Usage: python3 scripts/commons_fetch.py posts/<folder> "File:Name.jpg=local-name.jpg" [...]
Saves <folder>/images/<local-name> (max 1800px) and updates <folder>/images/CREDITS.json.
"""
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

UA = {"User-Agent": "TimeCircuitsBot/0.1 (personal project)"}


def api(title: str) -> dict:
    q = ("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata"
         "&iiurlwidth=1600&format=json&titles=" + urllib.parse.quote(title))
    page = next(iter(json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA)))["query"]["pages"].values()))
    return page["imageinfo"][0]


def main(folder: str, pairs: list[str]) -> None:
    d = Path(folder) / "images"
    d.mkdir(parents=True, exist_ok=True)
    credits_file = d / "CREDITS.json"
    credits = json.loads(credits_file.read_text()) if credits_file.exists() else {}
    strip = lambda s: re.sub("<[^>]+>", "", s or "").strip()
    for pair in pairs:
        title, name = pair.rsplit("=", 1)
        info = api(title)
        m = info["extmetadata"]
        time.sleep(3)
        src = info.get("thumburl") or info["url"]
        im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(src, headers=UA)).read())).convert("RGB")
        im.thumbnail((1800, 1800))
        im.save(d / name, quality=90)
        credits[name] = {"title": title, "page": info["descriptionurl"],
                         "license": strip(m.get("LicenseShortName", {}).get("value")),
                         "artist": strip(m.get("Artist", {}).get("value"))[:120]}
        print(f"{name}: {im.size} · {credits[name]['license']} · {credits[name]['artist']}")
        time.sleep(5)
    credits_file.write_text(json.dumps(credits, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
