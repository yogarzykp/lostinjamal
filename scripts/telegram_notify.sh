#!/bin/bash
# Telegram outbound notification helper.
# Use for: training start/finish, HF push, eval start/result, commit push,
# code adjustments.
#
# Usage:
#   ./telegram_notify.sh <event_type> <title> [details_file]
#
# Examples:
#   ./telegram_notify.sh TRAIN_START "708e03d4 Qwen 0.5B"
#   ./telegram_notify.sh TRAIN_DONE  "zay-qennn-222" /tmp/zay-qennn-222.log
#   ./telegram_notify.sh EVAL_RESULT "708e03d4" /tmp/eval.log
#   ./telegram_notify.sh COMMIT_PUSH "fix: model_detection patch" branch_name
#   ./telegram_notify.sh ERROR       "Build failed" /tmp/build.log
#
# Env vars (both required, gracefully skips if missing):
#   TELEGRAM_BOT_TOKEN  — bot token from @BotFather
#   TELEGRAM_CHAT_ID    — target chat/user ID
#
# Auto-loads from .telegram.env in same dir / parent / /root if not set.

EVENT="${1:-UNKNOWN}"
TITLE="${2:-(no title)}"
DETAILS="${3:-}"

# Auto-source credentials (priority order)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for candidate in \
    "${SCRIPT_DIR}/.telegram.env" \
    "${SCRIPT_DIR}/../.telegram.env" \
    "/root/.telegram.env" \
    "/root/text-jagger/.telegram.env"; do
    if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] && [ -f "${candidate}" ]; then
        # shellcheck source=/dev/null
        source "${candidate}"
        break
    fi
done

TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="${TELEGRAM_CHAT_ID:-}"

if [ -z "$TOKEN" ] || [ -z "$CHAT_ID" ]; then
    echo "[telegram] skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set" >&2
    exit 0
fi

# Emoji per event
case "$EVENT" in
    TRAIN_START)   ICON="🚂" ;;
    TRAIN_DONE)    ICON="✅" ;;
    TRAIN_FAIL)    ICON="❌" ;;
    HF_PUSH)       ICON="📤" ;;
    EVAL_START)    ICON="🔍" ;;
    EVAL_RESULT)   ICON="📊" ;;
    COMMIT_PUSH)   ICON="📌" ;;
    ADJUST)        ICON="⚙️" ;;
    ERROR)         ICON="🚨" ;;
    INFO)          ICON="ℹ️" ;;
    *)             ICON="📋" ;;
esac

HOST=$(hostname 2>/dev/null || echo "unknown")
TS=$(date +"%H:%M:%S")
LINK_LINE=""

# Auto-extract useful info from details file
EXTRA=""
if [ -n "$DETAILS" ] && [ -f "$DETAILS" ]; then
    case "$EVENT" in
        TRAIN_DONE)
            EVAL=$(grep -oE 'best.*eval_loss[: ]+[0-9.]+|eval_loss[: ]+[0-9.]+' "$DETAILS" 2>/dev/null | tail -1)
            REPO=$(grep -oE 'Uploaded successfully to https://huggingface.co/[A-Za-z0-9/_-]+' "$DETAILS" 2>/dev/null | tail -1)
            RUNTIME=$(grep -oE 'train_runtime['\''\":]+[: ]+[0-9.]+' "$DETAILS" 2>/dev/null | tail -1)
            EXTRA="$EVAL"$'\n'"$RUNTIME"$'\n'"$REPO"
            ;;
        EVAL_RESULT)
            RESULTS=$(grep -A 18 'Test data evaluation results' "$DETAILS" 2>/dev/null | tail -18 | head -16)
            EXTRA="$RESULTS"
            ;;
        ERROR)
            TAIL=$(tail -10 "$DETAILS" 2>/dev/null)
            EXTRA="<pre>$TAIL</pre>"
            ;;
        TRAIN_FAIL)
            # Find last error/traceback
            ERR=$(grep -E "Error|OOM|Traceback|FAIL" "$DETAILS" 2>/dev/null | tail -5)
            EXTRA="$ERR"
            ;;
        COMMIT_PUSH)
            # DETAILS is the branch name in this case
            EXTRA="branch: $DETAILS"
            ;;
    esac
fi

# Compose message — Telegram limit ~4096 chars
MSG="${ICON} <b>${EVENT}</b> · <code>${HOST}</code> · ${TS}
<b>${TITLE}</b>"

if [ -n "$EXTRA" ]; then
    # Truncate at 3500 chars to leave room for title/icon
    EXTRA_TRUNC=$(echo "$EXTRA" | head -c 3500)
    MSG="${MSG}
${EXTRA_TRUNC}"
fi

# Send via Telegram Bot API
RESP=$(curl -s --max-time 15 \
    -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    -d "parse_mode=HTML" \
    --data-urlencode "text=${MSG}" 2>&1)

OK=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('ok','false'))" 2>/dev/null)
if [ "$OK" = "True" ] || [ "$OK" = "true" ]; then
    echo "[telegram] sent: $EVENT — $TITLE"
else
    echo "[telegram] failed: $RESP" >&2
fi
