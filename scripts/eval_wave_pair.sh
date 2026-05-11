#!/bin/bash
# Pairwise eval: winner vs ours for all 9 Wave 1+2 tasks.
# GRPO note: HIGHER eval_loss = WINNER (validator scoring.py line 78/97-98).
# Instruct/DPO: LOWER eval_loss = WINNER (standard NLL).
# Dual-repo single call ensures identical prompts (especially critical for GRPO).
#
# Usage: bash eval_wave_pair.sh [task_index]   # default: all 9
# Run from /root/G.O.D-eval-text/

set -uo pipefail

# task_id : task_type : winner_hk8 : our_repo : winner_published_test_loss
QUEUE=(
    "708e03d4-1a55-440a-ad2e-58f1284c5d61:Instruct:5G1efLqq:Gege24/zay-aug-708e03d4-v1:1.0882"
    "0bda471b-9209-4778-8587-5e10a46205d7:Instruct:5DLkfAsZ:Gege24/zay-aug-0bda471b-v1:1.7559"
    "71e64603-f641-40cb-b0fd-91a13dd117fa:Dpo:5Hosruax:Gege24/zay-aug-71e64603-v1:0.6922"
    "020b2f24-3214-461e-a24e-d9f9cf86669c:Grpo:5GU4Xkd3:Gege24/zay-aug-020b2f24-v1:0.9871"
    "0c5c7124-3e21-4487-b31c-0a1d63a2da51:Instruct:5GU4Xkd3:Gege24/zay-aug-0c5c7124-v1:1.5119"
    "8fbf4273-be63-4b90-8fa3-016b9f12bb1f:Grpo:5GU4Xkd3:Gege24/zay-aug-8fbf4273-v1:0.2308"
    "acd597ef-23a9-4713-8e3f-8a1bbbde5648:Instruct:5Ek3D5Jp:Gege24/zay-aug-acd597ef-v1:1.1017"
    "e84aca25-ebd0-4afd-af15-e489310011ef:Instruct:5G1efLqq:Gege24/zay-aug-e84aca25-v1:0.5566"
    "45d5ffd1-2744-436d-a1df-42af6d03913a:Dpo:5CSGKFBJ:Gege24/zay-aug-45d5ffd1-v1:0.0000"
)

TOURN_PREFIX="gradients-io-tournaments/tournament-tourn_864dc15fbbcbc151_20260507"
RESULT_LOG="/root/text-jagger/logs/eval_wave_pair_$(date +%Y%m%d_%H%M%S).log"
SUMMARY_TSV="/root/text-jagger/logs/eval_wave_pair_summary.tsv"
NOTIFY_SCRIPT="/root/text-jagger/scripts/telegram_notify.sh"

mkdir -p "$(dirname "$RESULT_LOG")"
echo "task_id	task_type	winner_repo	our_repo	winner_test_loss	our_test_loss	winner_published	verdict" > "$SUMMARY_TSV"
[ -f "$NOTIFY_SCRIPT" ] && bash "$NOTIFY_SCRIPT" MILESTONE "Wave 1+2 EVAL START" "9 tasks pairwise eval starting" || true

cd /root/G.O.D-eval-text/ || { echo "FATAL: cannot cd to G.O.D-eval-text"; exit 1; }

# Activate eval venv if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

START_IDX="${1:-0}"
END_IDX="${2:-${#QUEUE[@]}}"

for i in "${!QUEUE[@]}"; do
    if [ "$i" -lt "$START_IDX" ] || [ "$i" -ge "$END_IDX" ]; then continue; fi
    IFS=':' read -r tid ttype hk8 our_repo winner_pub <<< "${QUEUE[$i]}"
    n=$((i + 1))
    total=${#QUEUE[@]}
    winner_repo="${TOURN_PREFIX}-${tid}-${hk8}"

    echo ""
    echo "================================================================" | tee -a "$RESULT_LOG"
    echo "  [$n/$total] $tid ($ttype)" | tee -a "$RESULT_LOG"
    echo "  winner_hk: $hk8  winner_repo: $winner_repo" | tee -a "$RESULT_LOG"
    echo "  our_repo:  $our_repo" | tee -a "$RESULT_LOG"
    echo "  winner_published_test_loss: $winner_pub" | tee -a "$RESULT_LOG"
    echo "================================================================" | tee -a "$RESULT_LOG"

    EVAL_OUT="/tmp/eval_${tid:0:8}.out"
    python -m utils.run_evaluation --task_id "$tid" --models "$winner_repo" "$our_repo" \
        2>&1 | tee "$EVAL_OUT" | tee -a "$RESULT_LOG"
    EXIT_CODE=${PIPESTATUS[0]}

    # Parse losses from output (winner_repo first, our_repo second)
    WIN_LOSS=$(grep -oE "$winner_repo.*test_loss[^0-9]+[0-9.]+" "$EVAL_OUT" | tail -1 | grep -oE "[0-9.]+$")
    OUR_LOSS=$(grep -oE "$our_repo.*test_loss[^0-9]+[0-9.]+" "$EVAL_OUT" | tail -1 | grep -oE "[0-9.]+$")

    # Verdict
    if [ "$ttype" = "Grpo" ]; then
        # GRPO: higher = winner
        verdict="UNKNOWN"
        if [ -n "$WIN_LOSS" ] && [ -n "$OUR_LOSS" ]; then
            if (( $(echo "$OUR_LOSS > $WIN_LOSS" | bc -l) )); then verdict="WIN(higher)"; else verdict="LOSE(lower)"; fi
        fi
    else
        # Instruct/DPO: lower = winner
        verdict="UNKNOWN"
        if [ -n "$WIN_LOSS" ] && [ -n "$OUR_LOSS" ]; then
            if (( $(echo "$OUR_LOSS < $WIN_LOSS" | bc -l) )); then verdict="WIN(lower)"; else verdict="LOSE(higher)"; fi
        fi
    fi

    echo -e "${tid}\t${ttype}\t${winner_repo}\t${our_repo}\t${WIN_LOSS:-N/A}\t${OUR_LOSS:-N/A}\t${winner_pub}\t${verdict}" >> "$SUMMARY_TSV"
    echo "[VERDICT] $tid $ttype: winner=$WIN_LOSS  ours=$OUR_LOSS  $verdict" | tee -a "$RESULT_LOG"
    [ -f "$NOTIFY_SCRIPT" ] && bash "$NOTIFY_SCRIPT" EVAL_DONE "$tid ($ttype)" "winner=$WIN_LOSS ours=$OUR_LOSS $verdict" || true
done

echo ""
echo "================================================================"
echo "  EVAL COMPLETE — see $SUMMARY_TSV"
echo "================================================================"
cat "$SUMMARY_TSV"
[ -f "$NOTIFY_SCRIPT" ] && bash "$NOTIFY_SCRIPT" MILESTONE "Wave 1+2 EVAL DONE" "$(cat $SUMMARY_TSV)" || true
