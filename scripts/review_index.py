"""Build one approval page for several posts: python3 scripts/review_index.py posts/L*"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def section(folder: Path) -> str:
    post = json.loads((folder / "post.json").read_text())
    rel = folder.relative_to(ROOT / "posts")
    imgs = "".join(f'<img src="{rel}/slides/{f.name}" alt="">' for f in sorted((folder / "slides").glob("*.jpg")))
    li = lambda xs: "".join(f"<li>{html.escape(x)}</li>" for x in xs)
    notes = post.get("review_notes", [])
    reel = post.get("reel")
    reel_html = ""
    if reel and (folder / reel["file"]).exists():
        reel_html = (f'<details open><summary>Reel · {html.escape(reel.get("scheduled_at", "").replace("T", " "))} · '
                     f'status: {html.escape(reel.get("status", "draft"))}</summary><div class="reel">'
                     f'<video controls muted playsinline preload="metadata" src="{rel}/{reel["file"]}"></video>'
                     f'<pre>{html.escape(reel.get("caption", ""))}</pre></div></details>')
    return f"""<article id="{rel}"><h2>{html.escape(rel.name.split('-')[0])} · {html.escape(post['title'])}</h2>
<div class="meta">{html.escape(post.get('pillar', ''))} · {html.escape(post.get('scheduled', ''))}</div>
<div class="strip">{imgs}</div>
{reel_html}
<details open><summary>Caption</summary><pre>{html.escape(post['caption'])}</pre></details>
<details><summary>Sources ({len(post.get('sources', []))})</summary><ul>{li(post.get('sources', []))}</ul></details>
{f'<details open><summary>Notes for approval</summary><ul>{li(notes)}</ul></details>' if notes else ''}</article>"""


def main(folders: list[str]) -> None:
    body = "\n".join(section((ROOT / f).resolve()) for f in sorted(folders))
    out = ROOT / "posts" / "launch-review.html"
    out.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Launch review</title><style>
body{{margin:0;font-family:-apple-system,sans-serif;background:#f4f1ea;color:#1b1b1b;padding:32px 16px}}
main{{max-width:1100px;margin:0 auto}} h1{{margin:0 0 24px}} h2{{font-size:22px;margin:0 0 4px}}
article{{background:#fff;border-radius:10px;padding:20px 24px;margin-bottom:32px}} .meta{{color:#666;margin-bottom:16px}}
.strip{{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px}}
.strip img{{height:440px;aspect-ratio:4/5;scroll-snap-align:start;border-radius:6px;box-shadow:0 3px 14px rgba(0,0,0,.18)}}
details{{margin-top:14px}} .reel{{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}}
.reel video{{width:240px;aspect-ratio:9/16;border-radius:8px;background:#000}} .reel pre{{flex:1;min-width:220px}} summary{{font-weight:600;cursor:pointer}} pre{{white-space:pre-wrap;font:15px/1.5 -apple-system,sans-serif}}
li{{margin:4px 0;word-break:break-word}}
@media (prefers-color-scheme:dark){{body{{background:#161616;color:#eee}}article{{background:#222}}.meta{{color:#aaa}}}}
</style></head><body><main><h1>Time Circuits — launch posts</h1>{body}</main></body></html>""")
    print(out)


if __name__ == "__main__":
    main(sys.argv[1:])
