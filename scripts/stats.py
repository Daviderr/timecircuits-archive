"""Read-only stats for the account and its posts (nothing is published or changed).

Usage: /opt/anaconda3/bin/python3 scripts/stats.py [--save]
--save appends today's snapshot to strategy/metrics/history.csv (one row per post + one account row).
Basic counts (followers, likes, comments) need instagram_business_basic.
Reach / saves / shares / views need instagram_business_manage_insights; if missing, it says so.
"""
import csv
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import requests  # noqa: E402

from publish import api, env  # noqa: E402

INSIGHTS = "reach,saved,shares,total_interactions,views"


def get(url: str, **params) -> dict:
    return requests.get(url, params=params, timeout=30).json()


HISTORY = Path(__file__).resolve().parent.parent / "strategy" / "metrics" / "history.csv"
FIELDS = ["snapshot", "kind", "media_id", "published", "title", "followers", "reach", "views",
          "likes", "comments", "saved", "shares"]


def main() -> None:
    save = "--save" in sys.argv
    rows = []
    cfg = env()
    tok = cfg["IG_ACCESS_TOKEN"]
    me = get(f"{api(cfg)}/me", fields="username,followers_count,follows_count,media_count", access_token=tok)
    if "error" in me:
        raise SystemExit(f"Errore: {me['error'].get('message')}")
    print(f"@{me['username']} · follower {me.get('followers_count')} · seguiti {me.get('follows_count')} · post {me.get('media_count')}\n")
    today = str(date.today())
    rows.append({"snapshot": today, "kind": "account", "followers": me.get("followers_count")})

    media = get(f"{api(cfg)}/me/media", fields="id,caption,timestamp,like_count,comments_count,permalink,media_product_type",
                limit=25, access_token=tok).get("data", [])
    insights_ok = True
    for m in sorted(media, key=lambda x: x["timestamp"]):
        title = (m.get("caption") or "").split("\n")[0][:55]
        kind = "reel" if m.get("media_product_type") == "REELS" else "post"
        line = f"{m['timestamp'][:10]} {kind:<4} ♥ {m.get('like_count', 0):>3}  💬 {m.get('comments_count', 0):>2}"
        vals = {}
        if insights_ok:
            ins = get(f"{api(cfg)}/{m['id']}/insights", metric=INSIGHTS, access_token=tok)
            if "error" in ins:
                insights_ok = False
                print(f"(insights non disponibili: {ins['error'].get('message', '')[:120]})\n")
            else:
                vals = {d["name"]: d["values"][0]["value"] for d in ins.get("data", [])}
                line += (f"  copertura {vals.get('reach', '-'):>5}  visualizz. {vals.get('views', '-'):>5}"
                         f"  salvati {vals.get('saved', '-'):>3}  condivisi {vals.get('shares', '-'):>3}")
        print(f"{line}  · {title}")
        rows.append({"snapshot": today, "kind": kind, "media_id": m["id"], "published": m["timestamp"][:10],
                     "title": title, "reach": vals.get("reach"), "views": vals.get("views"),
                     "likes": m.get("like_count"), "comments": m.get("comments_count"),
                     "saved": vals.get("saved"), "shares": vals.get("shares")})
    if save:
        HISTORY.parent.mkdir(parents=True, exist_ok=True)
        new = not HISTORY.exists()
        with HISTORY.open("a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS)
            if new:
                w.writeheader()
            w.writerows(rows)
        print(f"\nSnapshot salvato in {HISTORY.relative_to(HISTORY.parent.parent.parent)} ({len(rows)} righe)")


if __name__ == "__main__":
    main()
