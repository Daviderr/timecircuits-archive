"""One-time setup: the editor pastes the Instagram token (hidden), everything else is automatic.

Usage (from the project folder):  python3 scripts/setup_token.py

- asks for the token without showing it on screen
- checks it with Instagram (/me) and finds the account's user ID by itself
- writes the local .env (excluded from git)
- if the GitHub repo is already set up, offers to save IG_USER_ID and IG_ACCESS_TOKEN as repo secrets
Nothing is published.
"""
import getpass
import shutil
import subprocess
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
API_VERSION = "v23.0"


def main() -> None:
    token = getpass.getpass("Incolla il token di Instagram (non verrà mostrato) e premi Invio: ").strip()
    if not token:
        raise SystemExit("Nessun token inserito.")

    r = requests.get(f"https://graph.instagram.com/{API_VERSION}/me",
                     params={"fields": "user_id,username", "access_token": token}, timeout=30)
    data = r.json()
    if "error" in data or r.status_code >= 400:
        raise SystemExit(f"Token non valido: {data.get('error', {}).get('message', data)}")
    user_id, username = data["user_id"], data["username"]
    print(f"✓ Token valido per @{username} (ID {user_id})")
    if username != "timecircuits.archive":
        print("⚠️  Attenzione: il token non è dell'account @timecircuits.archive!")

    repo = ""
    if shutil.which("gh"):
        out = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                             cwd=ROOT, capture_output=True, text=True)
        repo = out.stdout.strip()

    env = ROOT / ".env"
    env.write_text(
        f"IG_USER_ID={user_id}\nIG_ACCESS_TOKEN={token}\nIG_API_VERSION={API_VERSION}\n"
        f"HOST_KIND=github\nHOST_GITHUB_REPO={repo}\n")
    env.chmod(0o600)
    print("✓ File .env salvato (solo sul tuo Mac, escluso da GitHub)")

    if repo and input(f"Salvo ID e token anche come segreti del repository {repo}? [s/N] ").lower() == "s":
        for name, value in (("IG_USER_ID", user_id), ("IG_ACCESS_TOKEN", token)):
            subprocess.run(["gh", "secret", "set", name, "--repo", repo], input=value, text=True,
                           cwd=ROOT, check=True, capture_output=True)
            print(f"✓ Segreto {name} salvato su GitHub")
    elif not repo:
        print("GitHub non è ancora configurato: rilancia questo script dopo la parte C per salvare i segreti.")


if __name__ == "__main__":
    main()
