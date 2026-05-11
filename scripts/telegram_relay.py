"""
Telegram → Claude inbound relay.

Polls Telegram getUpdates API, forwards each message text to a running
`claude` session inside tmux (via `tmux send-keys`).

Setup (one-time on your laptop):
  1. Start claude inside tmux:
       tmux new -s claude
       (then inside: claude)
  2. Configure env (or source .telegram.env):
       export TELEGRAM_BOT_TOKEN=...
       export TELEGRAM_CHAT_ID=...
       export RELAY_TMUX_TARGET=claude       # tmux session/window name
  3. Run relay:
       python3 telegram_relay.py
  4. Send message via Telegram → forwarded to claude session

Filters (security):
  - Only accepts messages from configured TELEGRAM_CHAT_ID (your user)
  - Strips system commands matching SAFE_DENY_PATTERNS

Behavior:
  - Long-polls Telegram (timeout 25s, low CPU)
  - Persists last_update_id in /tmp/telegram_relay_state.json
  - Loops indefinitely; Ctrl+C to stop
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


STATE_PATH = Path("/tmp/telegram_relay_state.json")
POLL_TIMEOUT = 25  # long-poll seconds; Telegram returns ASAP when message arrives
LOOP_SLEEP_ON_ERR = 5

# Safety: deny patterns that should not be forwarded as-is to claude
SAFE_DENY_PATTERNS = [
    re.compile(r"rm\s+-rf"),
    re.compile(r"chmod\s+777"),
    re.compile(r"curl[^|]+\|\s*(bash|sh)"),
]


def load_env() -> tuple[str, str, str]:
    """Load credentials from env or .telegram.env."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    target = os.environ.get("RELAY_TMUX_TARGET", "claude").strip()

    if not token or not chat_id:
        # Try .telegram.env in script dir
        env_path = Path(__file__).parent / ".telegram.env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if k.strip() == "TELEGRAM_BOT_TOKEN" and not token:
                    token = v
                elif k.strip() == "TELEGRAM_CHAT_ID" and not chat_id:
                    chat_id = v
                elif k.strip() == "RELAY_TMUX_TARGET":
                    target = v

    if not token or not chat_id:
        sys.exit("ERROR: Set TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID env or .telegram.env")
    return token, chat_id, target


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {"last_update_id": 0}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state))


def get_updates(token: str, offset: int) -> list:
    """Poll Telegram. Returns list of update objects or [] on timeout."""
    import urllib.request, urllib.parse

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = urllib.parse.urlencode({
        "offset": offset,
        "timeout": POLL_TIMEOUT,
        "allowed_updates": json.dumps(["message"]),
    })
    req = urllib.request.Request(f"{url}?{params}", headers={"User-Agent": "telegram_relay/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=POLL_TIMEOUT + 5) as resp:
            data = json.loads(resp.read())
            if data.get("ok"):
                return data.get("result", [])
            print(f"[relay] Telegram API not ok: {data}", file=sys.stderr)
    except Exception as exc:
        print(f"[relay] getUpdates exception: {exc}", file=sys.stderr)
    return []


def is_message_allowed(msg: dict, allowed_chat_id: str) -> tuple[bool, str]:
    """Return (allowed, text). Filters: chat_id match + deny patterns + length."""
    chat = msg.get("chat", {})
    if str(chat.get("id", "")) != str(allowed_chat_id):
        return False, ""
    text = msg.get("text", "").strip()
    if not text:
        return False, ""
    if len(text) > 8000:
        return False, "(message too long, skipped)"
    for pattern in SAFE_DENY_PATTERNS:
        if pattern.search(text):
            return False, "(denied by safety filter)"
    return True, text


def tmux_send(target: str, text: str) -> bool:
    """Send text + Enter to a tmux session/window."""
    # Send text literally (no shell expansion)
    try:
        subprocess.run(
            ["tmux", "send-keys", "-t", target, "-l", text],
            check=True, capture_output=True,
        )
        # Send Enter
        subprocess.run(
            ["tmux", "send-keys", "-t", target, "C-m"],
            check=True, capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as exc:
        err = exc.stderr.decode() if exc.stderr else str(exc)
        print(f"[relay] tmux send-keys failed: {err}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"[relay] tmux not installed — install: brew install tmux", file=sys.stderr)
        return False


def telegram_reply(token: str, chat_id: str, text: str) -> None:
    """Echo confirmation back to Telegram."""
    import urllib.request, urllib.parse

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=10)
    except Exception:
        pass


def main():
    token, chat_id, target = load_env()
    state = load_state()
    last_update_id = state.get("last_update_id", 0)

    print(f"[relay] Started. Listening for chat_id={chat_id}, forwarding to tmux={target}")
    print(f"[relay] State file: {STATE_PATH}")

    while True:
        try:
            updates = get_updates(token, last_update_id + 1)
            for upd in updates:
                last_update_id = max(last_update_id, upd.get("update_id", 0))
                msg = upd.get("message") or upd.get("edited_message")
                if not msg:
                    continue
                allowed, text = is_message_allowed(msg, chat_id)
                if not allowed:
                    if text:
                        print(f"[relay] rejected: {text}", file=sys.stderr)
                    continue
                # Forward to tmux
                ok = tmux_send(target, text)
                if ok:
                    snippet = text[:80] + ("…" if len(text) > 80 else "")
                    print(f"[relay] → tmux:{target}: {snippet}")
                    telegram_reply(token, chat_id, f"✓ forwarded: <code>{snippet}</code>")
                else:
                    telegram_reply(token, chat_id, "✗ failed to forward to claude session (tmux target not running?)")
            save_state({"last_update_id": last_update_id})
        except KeyboardInterrupt:
            print("[relay] stopped by user")
            break
        except Exception as exc:
            print(f"[relay] loop error: {exc}", file=sys.stderr)
            time.sleep(LOOP_SLEEP_ON_ERR)


if __name__ == "__main__":
    main()
