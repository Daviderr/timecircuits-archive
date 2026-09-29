"""Render a carousel post to 1080x1350 JPEG slides plus a review page.

Usage: python3 scripts/render.py posts/<folder>

Reads <folder>/post.json, writes <folder>/slides/NN.jpg and <folder>/review.html.
Uses the locally installed Google Chrome in headless mode (no extra deps besides Pillow).
"""
import html
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1080, 1350


def rich(text: str) -> str:
    """Escape text, then allow *italic* and **bold** markers."""
    import re
    t = html.escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")


def image_block(s: dict, folder: Path) -> str:
    """Optional licensed photo: {"file": "images/x.jpg", "credit": "...", "focus": "center 30%"}."""
    img = s.get("image")
    if not img:
        return ""
    uri = (folder / img["file"]).resolve().as_uri()
    focus = html.escape(img.get("focus", "center"))
    credit = f'<div class="credit">{html.escape(img["credit"])}</div>' if img.get("credit") else ""
    if s.get("type") == "cover":
        return f'<div class="bg-photo" style="background-image:url(\'{uri}\');background-position:{focus}"></div>{credit}'
    return f'<figure class="photo"><div class="img" style="background-image:url(\'{uri}\');background-position:{focus}"></div>{credit}</figure>'


def slide_inner(s: dict, folder: Path) -> str:
    kind = s.get("type", "text")
    parts = []
    if kind != "cover":
        parts.append(image_block(s, folder))
    if kind == "year":
        parts.append(f'<div class="year">{html.escape(s["year"])}</div>')
    if s.get("kicker"):
        parts.append(f'<div class="kicker">{rich(s["kicker"])}</div>')
    if s.get("title"):
        tag = "h1" if kind == "cover" else "h2"
        parts.append(f"<{tag}>{rich(s['title'])}</{tag}>")
    if kind == "cover" and s.get("body"):
        parts.append('<div class="rule"></div>')
    if s.get("body"):
        parts.append(f'<div class="body">{rich(s["body"])}</div>')
    if kind == "cta":
        pills = "".join(f'<div class="pill">{html.escape(a)}</div>' for a in s.get("actions", []))
        parts.append(f'<div class="actions">{pills}</div>')
        if s.get("next"):
            parts.append(f'<div class="next">Next story<br><b>{rich(s["next"])}</b></div>')
    return "\n".join(parts)


def slide_html(s: dict, i: int, n: int, brand: dict, css: str, folder: Path) -> str:
    c = brand["colors"]
    has_img = " has-img" if s.get("image") else ""
    cover_bg = image_block(s, folder) if s.get("type") == "cover" else ""
    last = i == n
    bottom_right = "" if last else '<div class="swipe">Swipe<span>&rarr;</span></div>'
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>:root{{--bg:{c['bg']};--paper:{c['paper']};--gold:{c['gold']};--muted:{c['muted']};}}
{css}</style></head><body>
<div class="slide t-{html.escape(s.get('type', 'text'))}{has_img}">
  {cover_bg}
  <div class="top"><div>{html.escape(brand['name'])}</div><div class="page"><b>{i:02d}</b> / {n:02d}</div></div>
  <div class="content">{slide_inner(s, folder)}</div>
  <div class="bottom"><div>{html.escape(brand['handle'])}</div>{bottom_right}</div>
  <div class="progress"><i style="width:{i / n * 100:.1f}%"></i></div>
</div></body></html>"""


def screenshot(html_path: Path, png_path: Path) -> None:
    subprocess.run(
        [CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
         f"--window-size={W},{H}", "--virtual-time-budget=5000",
         f"--screenshot={png_path}", html_path.as_uri()],
        check=True, capture_output=True,
    )


def review_page(post: dict, files: list[str]) -> str:
    imgs = "\n".join(f'<img src="slides/{f}" alt="slide {k + 1}">' for k, f in enumerate(files))
    sources = "".join(f"<li>{html.escape(s)}</li>" for s in post.get("sources", []))
    notes = "".join(f"<li>{html.escape(s)}</li>" for s in post.get("review_notes", []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Review: {html.escape(post['title'])}</title>
<style>
body{{margin:0;font-family:-apple-system,Inter,sans-serif;background:#f4f1ea;color:#1b1b1b;padding:32px 16px}}
main{{max-width:1100px;margin:0 auto}} h1{{font-size:26px;margin:0 0 4px}} .meta{{color:#666;margin-bottom:24px}}
.strip{{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px}}
.strip img{{height:520px;aspect-ratio:4/5;scroll-snap-align:start;border-radius:6px;box-shadow:0 4px 18px rgba(0,0,0,.18)}}
section{{background:#fff;border-radius:8px;padding:20px 24px;margin-top:24px}}
pre{{white-space:pre-wrap;font:15px/1.5 -apple-system,sans-serif;margin:0}}
@media (prefers-color-scheme:dark){{body{{background:#161616;color:#eee}}section{{background:#222}}.meta{{color:#aaa}}}}
</style></head><body><main>
<h1>{html.escape(post['title'])}</h1>
<div class="meta">{html.escape(post.get('pillar', ''))} · planned {html.escape(post.get('scheduled', 'TBD'))} · {len(files)} slides</div>
<div class="strip">{imgs}</div>
<section><h3>Caption</h3><pre>{html.escape(post['caption'])}</pre></section>
<section><h3>Sources</h3><ul>{sources}</ul></section>
{f'<section><h3>Notes for approval</h3><ul>{notes}</ul></section>' if notes else ''}
</main></body></html>"""


def main(folder: str) -> None:
    d = (ROOT / folder).resolve()
    post = json.loads((d / "post.json").read_text())
    brand = json.loads((ROOT / "brand.json").read_text())
    css = (ROOT / "templates" / "slide.css").read_text()
    out = d / "slides"
    out.mkdir(exist_ok=True)
    for old in out.glob("*.jpg"):
        old.unlink()

    slides = post["slides"]
    n = len(slides)
    files = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, s in enumerate(slides, 1):
            h = Path(tmp) / f"{i:02d}.html"
            p = Path(tmp) / f"{i:02d}.png"
            h.write_text(slide_html(s, i, n, brand, css, d))
            screenshot(h, p)
            name = f"{i:02d}.jpg"
            Image.open(p).convert("RGB").crop((0, 0, W, H)).save(out / name, "JPEG", quality=92)
            files.append(name)
            print(f"rendered {name}")

    (d / "review.html").write_text(review_page(post, files))
    print(f"review page: {d / 'review.html'}")


if __name__ == "__main__":
    main(sys.argv[1])
