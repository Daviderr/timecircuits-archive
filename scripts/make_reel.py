"""Turn a carousel into a 9:16 Reel (MP4) with the same slides and crossfades.

Usage: /opt/anaconda3/bin/python3 scripts/make_reel.py posts/<folder> [--time 19:00]

Writes <folder>/reel/reel.mp4 and adds a "reel" block to post.json (caption + schedule, same day as
the carousel at --time). The Reel needs its OWN approval ("reel.approved_at") before it can be published.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import ROOT, H, W, screenshot, slide_html  # noqa: E402

RW, RH = 1080, 1920  # Reel canvas
FIRST, MID, LAST, FADE = 3.0, 3.2, 3.0, 0.4  # seconds
FFMPEG = "/opt/homebrew/bin/ffmpeg"


def reel_caption(post: dict) -> str:
    lines = post["caption"].strip().split("\n")
    hook = lines[0]
    tags = lines[-1] if lines[-1].startswith("#") else ""
    return f"{hook}\n\nThe full story is in our carousel on the profile. ⌚\n\n{tags}".strip()


def main(folder: str, publish_time: str) -> None:
    d = (ROOT / folder).resolve()
    post_file = d / "post.json"
    post = json.loads(post_file.read_text())
    brand = json.loads((ROOT / "brand.json").read_text())
    css = (ROOT / "templates" / "slide.css").read_text()
    slides = post["slides"]
    n = len(slides)
    out_dir = d / "reel"
    out_dir.mkdir(exist_ok=True)
    bg = brand["colors"]["bg"]

    with tempfile.TemporaryDirectory() as tmp:
        frames = []
        for i, s in enumerate(slides, 1):
            h, p = Path(tmp) / f"{i:02d}.html", Path(tmp) / f"{i:02d}.png"
            h.write_text(slide_html(s, i, n, brand, css, d, reel=True))
            screenshot(h, p)
            canvas = Image.new("RGB", (RW, RH), bg)
            canvas.paste(Image.open(p).convert("RGB").crop((0, 0, W, H)), (0, (RH - H) // 2))
            f = Path(tmp) / f"frame{i:02d}.png"
            canvas.save(f)
            frames.append(f)

        durs = [FIRST] + [MID] * (n - 2) + [LAST]
        cmd = [FFMPEG, "-y", "-loglevel", "error"]
        for f, dur in zip(frames, durs):
            cmd += ["-loop", "1", "-t", f"{dur + FADE:.2f}", "-i", str(f)]
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        # chain crossfades: each transition starts FADE before the end of the running timeline
        chain, prev, t = [], "[0:v]", 0.0
        for k in range(1, n):
            t += durs[k - 1]
            label = f"[v{k}]"
            chain.append(f"{prev}[{k}:v]xfade=transition=fade:duration={FADE}:offset={t:.2f}{label}")
            prev = label
        total = sum(durs) + FADE
        chain.append(f"{prev}format=yuv420p,fps=30[vout]")
        cmd += ["-filter_complex", ";".join(chain), "-map", "[vout]", "-map", f"{n}:a",
                "-c:v", "libx264", "-profile:v", "high", "-crf", "20", "-preset", "medium",
                "-c:a", "aac", "-b:a", "128k", "-shortest", "-t", f"{total:.2f}",
                "-movflags", "+faststart", str(out_dir / "reel.mp4")]
        subprocess.run(cmd, check=True)

    date = post["scheduled_at"].split("T")[0]
    reel = post.get("reel", {})
    reel.update(file="reel/reel.mp4", caption=reel_caption(post),
                scheduled_at=f"{date}T{publish_time}", share_to_feed=False)
    reel.setdefault("status", "draft")
    post["reel"] = reel
    post_file.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
    size = (out_dir / "reel.mp4").stat().st_size / 1e6
    print(f"reel: {out_dir / 'reel.mp4'} · {total:.1f}s · {size:.1f} MB · scheduled {reel['scheduled_at']}")


if __name__ == "__main__":
    args = sys.argv[1:]
    when = args[args.index("--time") + 1] if "--time" in args else "19:00"
    main(args[0], when)
