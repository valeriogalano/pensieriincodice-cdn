#!/bin/bash

# Accetta il nome dell'episodio come parametro
if [ -z "$1" ]; then
    echo "Errore: è necessario fornire il nome dell'episodio come parametro."
    exit 1
fi

EPISODE_NAME=$1

# Scarica il file 'ggml-large-v3.bin' solo se non esiste già
if [ ! -f ./models/ggml-large-v3.bin ]; then
    curl -o ./models/ggml-large-v3.bin -L 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin'
    if [ $? -eq 0 ]; then
        echo "Download completato con successo."
    else
        echo "Errore durante il download del file ggml-large-v3.bin."
        exit 1
    fi
else
    echo "Il file ggml-large-v3.bin esiste già, non è necessario scaricarlo."
fi

# Converte il file MP3 in WAV con il nome dell'episodio
ffmpeg -i ../public/episodes/${EPISODE_NAME}.mp3 -acodec pcm_s16le -ar 16000 -ac 1 ${EPISODE_NAME}.wav
if [ $? -eq 0 ]; then
    echo "Conversione MP3 to WAV completata con successo."
else
    echo "Errore durante la conversione del file MP3 in WAV."
    exit 1
fi

# Esegue Whisper per trascrivere il file audio
./whisper --language it -t 7 --print-colors --max-len 25 --split-on-word true --model ./models/ggml-large-v3.bin --output-srt --file ${EPISODE_NAME}.wav
if [ $? -eq 0 ]; then
    echo "Trascrizione completata con successo."
    # Sposta il file SRT generato nella directory transcripts
    mv ${EPISODE_NAME}.wav.srt ../public/transcripts/${EPISODE_NAME}.srt
else
    echo "Errore durante la trascrizione del file audio."
    exit 1
fi

# Cancella file WAV temporaneo
rm ${EPISODE_NAME}.wav
