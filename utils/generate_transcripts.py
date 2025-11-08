import os
import whisper

def generate_transcripts(episodes_dir, transcripts_dir):
    # Carica il modello di Whisper
    model = whisper.load_model("large")
    # Assicurati che la cartella dei trascritti esista
    os.makedirs(transcripts_dir, exist_ok=True)

    # Itera sui file nella cartella degli episodi
    for filename in os.listdir(episodes_dir):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(episodes_dir, filename)
            srt_filename = f"{os.path.splitext(filename)[0]}.srt"
            srt_path = os.path.join(transcripts_dir, srt_filename)

            # Controlla se il file SRT già esiste
            if not os.path.exists(srt_path):
                print(f"Trascrizione di {filename} in corso...")
                result = model.transcribe(
                    mp3_path,
                    language="it",
                    temperature=0.0,
                    beam_size=5,
                    best_of=5,
                    initial_prompt="Trascrizione in italiano con punteggiatura corretta."
                )
                with open(srt_path, 'w', encoding='utf-8') as srt_file:
                    for i, segment in enumerate(result['segments']):
                        srt_file.write(f"{i+1}\n")
                        srt_file.write(f"{segment['start']:.3f} --> {segment['end']:.3f}\n")
                        srt_file.write(f"{segment['text']}\n\n")
                print(f"Trascrizione di {filename} completata e salvata in {srt_filename}.")
            else:
                print(f"La trascrizione per {filename} esiste già. Saltando...")

if __name__ == "__main__":
    generate_transcripts("./public/episodes", "./public/transcripts")