#!/bin/bash

set -euo pipefail

EPISODES_DIR="../../public/episodes"
TRANSCRIPTS_DIR="../../public/transcripts"
MODEL_NAME="ggml-large-v3.bin"
MODEL_PATH="./models/$MODEL_NAME"
WHISPER_BIN="../whisper"

mkdir -p "$(dirname "$MODEL_PATH")" "$TRANSCRIPTS_DIR"

# Scarica il modello Whisper solo se non esiste già
if [ ! -f "$MODEL_PATH" ]; then
  echo "Modello non trovato. Download in corso..."
  if curl -fSL -o "$MODEL_PATH" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$MODEL_NAME"; then
    echo "Download completato con successo."
  else
    echo "Errore durante il download del file $MODEL_NAME." >&2
    exit 1
  fi
else
  echo "Il file $MODEL_NAME esiste già, non è necessario scaricarlo."
fi

process_episode() {
  local EPISODE_NAME="$1"

  local MP3_PATH="$EPISODES_DIR/${EPISODE_NAME}.mp3"
  local WAV_PATH="${EPISODE_NAME}.wav"
  local OUT_SRT_TEMP="${WAV_PATH}.srt"
  local OUT_SRT_FINAL="$TRANSCRIPTS_DIR/${EPISODE_NAME}.srt"

  if [ ! -f "$MP3_PATH" ]; then
    echo "Errore: file non trovato: $MP3_PATH" >&2
    return 1
  fi

  if [ -f "$OUT_SRT_FINAL" ]; then
    echo "Trascrizione per ${EPISODE_NAME} già presente. Saltando..."
    return 0
  fi

  echo "[${EPISODE_NAME}] Conversione MP3 -> WAV..."
  if ffmpeg -hide_banner -loglevel error -i "$MP3_PATH" -acodec pcm_s16le -ar 16000 -ac 1 "$WAV_PATH"; then
    echo "[${EPISODE_NAME}] Conversione completata."
  else
    echo "[${EPISODE_NAME}] Errore durante la conversione MP3 in WAV." >&2
    return 1
  fi

  echo "[${EPISODE_NAME}] Trascrizione con whisper..."
  if "$WHISPER_BIN" -l it -t 7 --model "$MODEL_PATH" \
      --output-srt --beam-size 5 --best-of 5 \
      --split-on-word --max-len 15 \
      --prompt 'Trascrizione in italiano con punteggiatura corretta' \
      --file "$WAV_PATH"; then
    echo "[${EPISODE_NAME}] Trascrizione completata."
    mv "$OUT_SRT_TEMP" "$OUT_SRT_FINAL"
  else
    echo "[${EPISODE_NAME}] Errore durante la trascrizione del file audio." >&2
    rm -f "$WAV_PATH"
    return 1
  fi

  # Pulisce file temporaneo WAV
  rm -f "$WAV_PATH"
}

if [ $# -ge 1 ]; then
  # Modalità singolo episodio
  process_episode "$1"
  exit $?
else
  # Modalità batch: cerca tutte le tracce MP3 e genera solo le trascrizioni mancanti
  shopt -s nullglob
  mp3_files=("$EPISODES_DIR"/*.mp3)
  if [ ${#mp3_files[@]} -eq 0 ]; then
    echo "Nessun file MP3 trovato in $EPISODES_DIR. Nulla da fare."
    exit 0
  fi

  to_process=0
  for mp3 in "${mp3_files[@]}"; do
    base=$(basename "$mp3")
    name="${base%.mp3}"
    if [ ! -f "$TRANSCRIPTS_DIR/${name}.srt" ]; then
      ((to_process++)) || true
    fi
  done

  if [ $to_process -eq 0 ]; then
    echo "Tutte le trascrizioni sono già presenti in $TRANSCRIPTS_DIR."
    exit 0
  fi

  echo "Verranno generate $to_process trascrizioni mancanti..."
  for mp3 in "${mp3_files[@]}"; do
    base=$(basename "$mp3")
    name="${base%.mp3}"
    if [ ! -f "$TRANSCRIPTS_DIR/${name}.srt" ]; then
      process_episode "$name" || exit 1
    else
      echo "Trascrizione per ${name} già presente. Saltando..."
    fi
  done
fi
