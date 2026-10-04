"""Publish an APPROVED carousel to Instagram (Instagram API with Instagram Login).

Usage:
  python3 scripts/publish.py posts/<folder>            # dry run: checks everything, publishes nothing
  python3 scripts/publish.py posts/<folder> --publish  # really publishes
  python3 scripts/publish.py --due                     # publish the next approved carousel or Reel whose time has come (GitHub Actions)
  python3 scripts/publish.py posts/<folder> --reel     # dry run of the post's Reel (add --publish to post it)
  python3 scripts/publish.py --refresh-token           # renew the 60-day token (updates .env)
  python3 scripts/publish.py --print-refreshed-token   # renew and print only the new token (used by GitHub Actions)
  python3 scripts/publish.py --whoami                  # check the token/account

Safety: refuses any post whose post.json doesn't have "status": "approved" and an "approved_at" date.
A Reel needs its own approval ("reel": {"status": "approved", "approved_at": ...}) and goes out only after its carousel.
Config lives in .env (see .env.example); never commit it.
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent.parent
MAX_SLIDES = 10  # carousel limit for the API


def env() -> dict:
    cfg = {}
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip()
    cfg.update({k: v for k, v in os.environ.items() if k.startswith(("IG_", "HOST_"))})
    return cfg


def api(cfg: dict) -> str:
    return f"https://graph.instagram.com/{cfg.get('IG_API_VERSION', 'v23.0')}"


def call(method: str, url: str, **params) -> dict:
    r = requests.request(method, url, params=params, timeout=60)
    data = r.json()
    if r.status_code >= 400 or "error" in data:
        raise SystemExit(f"Instagram API error: {data.get('error', data)}")
    return data


def upload_public(path: Path, cfg: dict) -> str:
    """Put a JPEG at a public URL (Instagram downloads it from there). Host chosen in .env."""
    host = cfg.get("HOST_KIND")
    if host == "github":
        # Public repo: slides are committed, Instagram downloads them from raw.githubusercontent.com
        branch = cfg.get("HOST_GITHUB_BRANCH", "main")
        return f"https://raw.githubusercontent.com/{cfg['HOST_GITHUB_REPO']}/{branch}/{path.relative_to(ROOT).as_posix()}"
    if host == "base_url":
        # Files already synced to a public web folder: HOST_BASE_URL + posts/<folder>/slides/NN.jpg
        return cfg["HOST_BASE_URL"].rstrip("/") + "/" + path.relative_to(ROOT).as_posix()
    raise SystemExit("Image hosting not configured yet (HOST_KIND in .env). See docs/setup-instagram.md, Fase 5.")


def wait_ready(cfg: dict, container_id: str, tries: int = 30, delay: int = 5) -> None:
    for _ in range(tries):
        status = call("GET", f"{api(cfg)}/{container_id}", fields="status_code",
                      access_token=cfg["IG_ACCESS_TOKEN"]).get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            raise SystemExit(f"Container {container_id} failed: {status}")
        time.sleep(delay)
    raise SystemExit(f"Container {container_id} not ready after {tries * delay}s")


def publish(folder: str, really: bool) -> None:
    d = (ROOT / folder).resolve()
    post_file = d / "post.json"
    post = json.loads(post_file.read_text())
    slides = sorted((d / "slides").glob("*.jpg"))

    problems = []
    if post.get("status") != "approved" or not post.get("approved_at"):
        problems.append('not approved by the editor (needs "status": "approved" + "approved_at")')
    if not 2 <= len(slides) <= MAX_SLIDES:
        problems.append(f"{len(slides)} slides (carousel needs 2-{MAX_SLIDES})")
    if len(post.get("caption", "")) > 2200:
        problems.append("caption over 2,200 characters")
    if post.get("caption", "").count("#") > 30:
        problems.append("more than 30 hashtags")
    if problems:
        raise SystemExit("STOP, not publishing:\n - " + "\n - ".join(problems))

    print(f"OK: '{post['title']}' · {len(slides)} slides · approved {post['approved_at']}")
    if not really:
        print("Dry run only. Add --publish to post it for real.")
        return

    cfg = env()
    uid, token = cfg["IG_USER_ID"], cfg["IG_ACCESS_TOKEN"]
    children = []
    for s in slides:
        url = upload_public(s, cfg)
        c = call("POST", f"{api(cfg)}/{uid}/media", image_url=url, is_carousel_item="true", access_token=token)
        children.append(c["id"])
        print(f"  item {s.name} → {c['id']}")
    for c in children:
        wait_ready(cfg, c)
    carousel = call("POST", f"{api(cfg)}/{uid}/media", media_type="CAROUSEL",
                    children=",".join(children), caption=post["caption"], access_token=token)
    wait_ready(cfg, carousel["id"])
    media = call("POST", f"{api(cfg)}/{uid}/media_publish", creation_id=carousel["id"], access_token=token)
    link = call("GET", f"{api(cfg)}/{media['id']}", fields="permalink", access_token=token).get("permalink")

    post.update(status="published", published_at=datetime.now(ZoneInfo("Europe/Rome")).isoformat(timespec="minutes"),
                media_id=media["id"], permalink=link)
    post_file.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
    print(f"PUBLISHED: {link}")


def publish_reel(folder: str, really: bool) -> None:
    d = (ROOT / folder).resolve()
    post_file = d / "post.json"
    post = json.loads(post_file.read_text())
    reel = post.get("reel") or {}
    video = d / reel.get("file", "reel/reel.mp4")

    problems = []
    if reel.get("status") != "approved" or not reel.get("approved_at"):
        problems.append('Reel not approved by the editor (needs reel.status "approved" + reel.approved_at)')
    if post.get("status") != "published":
        problems.append("its carousel is not published yet (the Reel always goes out after it)")
    if not video.exists():
        problems.append(f"video file missing: {video.name}")
    if len(reel.get("caption", "")) > 2200:
        problems.append("Reel caption over 2,200 characters")
    if problems:
        raise SystemExit("STOP, not publishing the Reel:\n - " + "\n - ".join(problems))

    print(f"OK: Reel of '{post['title']}' · {video.stat().st_size / 1e6:.1f} MB · approved {reel['approved_at']}")
    if not really:
        print("Dry run only. Add --publish to post it for real.")
        return

    cfg = env()
    uid, token = cfg["IG_USER_ID"], cfg["IG_ACCESS_TOKEN"]
    c = call("POST", f"{api(cfg)}/{uid}/media", media_type="REELS", video_url=upload_public(video, cfg),
             caption=reel["caption"], share_to_feed=str(reel.get("share_to_feed", False)).lower(), access_token=token)
    wait_ready(cfg, c["id"], tries=60, delay=10)  # video processing can take a few minutes
    media = call("POST", f"{api(cfg)}/{uid}/media_publish", creation_id=c["id"], access_token=token)
    link = call("GET", f"{api(cfg)}/{media['id']}", fields="permalink", access_token=token).get("permalink")
    reel.update(status="published", published_at=datetime.now(ZoneInfo("Europe/Rome")).isoformat(timespec="minutes"),
                media_id=media["id"], permalink=link)
    post["reel"] = reel
    post_file.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
    print(f"PUBLISHED REEL: {link}")


def due_reels() -> list[Path]:
    """Approved Reels whose carousel is already out and whose own time (Europe/Rome) has passed."""
    now = datetime.now(ZoneInfo("Europe/Rome"))
    due = []
    for f in sorted((ROOT / "posts").glob("*/post.json")):
        post = json.loads(f.read_text())
        reel = post.get("reel") or {}
        if post.get("status") != "published" or reel.get("status") != "approved" or not reel.get("approved_at"):
            continue
        when = reel.get("scheduled_at")
        tz = ZoneInfo(post.get("timezone", "Europe/Rome"))
        if when and datetime.fromisoformat(when).replace(tzinfo=tz) <= now:
            due.append(f.parent)
    return due


def due_posts() -> list[Path]:
    """Approved, automatic, not yet published posts whose scheduled time (Europe/Rome) has passed."""
    now = datetime.now(ZoneInfo("Europe/Rome"))
    due = []
    for f in sorted((ROOT / "posts").glob("*/post.json")):
        post = json.loads(f.read_text())
        if post.get("status") != "approved" or post.get("publish_mode", "auto") == "manual":
            continue
        when = post.get("scheduled_at")
        tz = ZoneInfo(post.get("timezone", "Europe/Rome"))
        if when and datetime.fromisoformat(when).replace(tzinfo=tz) <= now:
            due.append(f.parent)
    return due


def refresh(cfg: dict) -> dict:
    return call("GET", "https://graph.instagram.com/refresh_access_token",
                grant_type="ig_refresh_token", access_token=cfg["IG_ACCESS_TOKEN"])


def main() -> None:
    args = sys.argv[1:]
    if "--due" in args:
        due, reels = due_posts(), due_reels()
        print(f"{len(due)} carousel(s) and {len(reels)} Reel(s) due")
        # at most one item per run, carousels first, so a backlog never floods the feed
        if due:
            publish(str(due[0].relative_to(ROOT)), really=True)
        elif reels:
            publish_reel(str(reels[0].relative_to(ROOT)), really=True)
        return
    if "--print-refreshed-token" in args:
        print(refresh(env())["access_token"])
        return
    if "--whoami" in args:
        cfg = env()
        print(call("GET", f"{api(cfg)}/me", fields="user_id,username", access_token=cfg["IG_ACCESS_TOKEN"]))
    elif "--refresh-token" in args:
        cfg = env()
        new = refresh(cfg)
        f = ROOT / ".env"
        f.write_text("\n".join(f"IG_ACCESS_TOKEN={new['access_token']}" if l.startswith("IG_ACCESS_TOKEN=") else l
                               for l in f.read_text().splitlines()) + "\n")
        print(f"Token renewed, valid for {new.get('expires_in', 0) // 86400} days.")
    elif args and "--reel" in args:
        publish_reel(args[0], really="--publish" in args)
    elif args:
        publish(args[0], really="--publish" in args)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
