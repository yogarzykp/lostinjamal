#!/usr/bin/env bash
# Fetch one G.O.D task's train/test data by task id, into a local bank.
#
#   ops/smoke/fetch_task_dataset.sh <task_id> [dest_dir]        default dest: ops/smoke/datasets_bank
#
# Why this exists. Nothing under ops/smoke fetches a dataset: every runner reads a pre-placed
# file under /cache/datasets on the GPU box. On 2026-09-14 the box was shut down with the
# gate's default dataset (dd558022) living only on its disk, and a pull started three minutes
# too late landed nothing. It was recovered because the task was still live on the auditing
# API — but its links are presigned and expire, and re-querying does not refresh an expired
# one. So: fetch by task id while the task is live, keep the BODY, never keep the link.
#
# Provisioning a new box:
#   ops/smoke/fetch_task_dataset.sh dd558022-496c-4779-8fef-118689e7a227
#   scp ops/smoke/datasets_bank/dd558022*_data.json root@<box>:/root/cache/datasets/
#
# The bank is gitignored: it is tournament data, tens of MB per task, and not ours to publish.
set -uo pipefail

TASK="${1:?usage: $0 <task_id> [dest_dir]}"
DEST="${2:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/datasets_bank}"
API="https://api.gradients.io/auditing/tasks/$TASK"
mkdir -p "$DEST"

META="$(curl -sS -m 30 "$API")" || { echo "fetch aborted: the auditing API did not answer for $TASK"; exit 2; }
STATUS="$(printf '%s' "$META" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("status",""))' 2>/dev/null)"
[ -n "$STATUS" ] || { echo "fetch aborted: no task record for $TASK"; printf '%s\n' "$META" | head -c 300; echo; exit 2; }
echo "task $TASK: status=$STATUS"

rc=0
for pair in "training_data:_train_data.json" "test_data:_test_data.json"; do
  key="${pair%%:*}"; suffix="${pair##*:}"
  URL="$(printf '%s' "$META" | python3 -c "import sys,json; print(json.load(sys.stdin).get('$key') or '')")"
  if [ -z "$URL" ]; then echo "  $key: no link on the record (expired or never set)"; rc=1; continue; fi
  OUT="$DEST/${TASK}${suffix}"
  # The link is a credential: it goes to curl and nowhere else — not to the log, not to disk.
  CODE="$(curl -sS -m 900 -o "$OUT" -w '%{http_code}' "$URL")" || CODE="curl-failed"
  if [ "$CODE" != "200" ]; then echo "  $key: HTTP $CODE — the link has probably expired"; rm -f "$OUT"; rc=1; continue; fi
  ROWS="$(python3 -c "import json; d=json.load(open('$OUT')); print(len(d) if isinstance(d,list) else 'obj')" 2>/dev/null)" \
    || { echo "  $key: body is not JSON — discarded"; rm -f "$OUT"; rc=1; continue; }
  echo "  $key: OK  $(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT") bytes  rows=$ROWS  -> $OUT"
done
exit $rc
