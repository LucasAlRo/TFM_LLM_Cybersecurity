#!/usr/bin/env bash
MODEL="$1"; PROMPT_FILE="$2"; INPUT_FILE="$3"; OUT_TXT="$4"; OUT_CSV="$5"

PROMPT=$(cat "$PROMPT_FILE")
INPUT=$(cat "$INPUT_FILE")
PAYLOAD="${PROMPT}\n\n=== INPUT ===\n${INPUT}"

TMP=$(mktemp)
printf "%b" "$PAYLOAD" | ollama generate --model "$MODEL" --json | tee "$TMP" > /dev/null

mkdir -p "$(dirname "$OUT_TXT")"
jq -r 'select(.response!=null) | .response' "$TMP" > "$OUT_TXT"
jq -r 'select(.done==true)' "$TMP" > "${TMP}.last"

TOTAL=$(jq -r '.total_duration' "${TMP}.last")
LOAD=$(jq -r '.load_duration // empty' "${TMP}.last")
PEVALC=$(jq -r '.prompt_eval_count' "${TMP}.last")
PEVALD=$(jq -r '.prompt_eval_duration' "${TMP}.last")
EVALC=$(jq -r '.eval_count' "${TMP}.last")
EVALD=$(jq -r '.eval_duration' "${TMP}.last")

mkdir -p "$(dirname "$OUT_CSV")"
if [ ! -f "$OUT_CSV" ]; then
  echo "modelo,total_ns,load_ns,prompt_eval_count,prompt_eval_ns,eval_count,eval_ns" > "$OUT_CSV"
fi
echo "$MODEL,$TOTAL,$LOAD,$PEVALC,$PEVALD,$EVALC,$EVALD" >> "$OUT_CSV"

rm -f "$TMP" "${TMP}.last"
