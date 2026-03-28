<div align="center">
  <img src="https://cdn.pensieriincodice.it/images/pensieriincodice-locandina.png" alt="Logo Progetto" width="150"/>
  <h1>Pensieri In Codice — CDN</h1>
  <p>Repository CDN per ospitare e servire asset statici (immagini, audio, trascrizioni) del podcast <a href="https://pensieriincodice.it/">pensieriincodice.it</a>.</p>
  <p>
    <img src="https://img.shields.io/github/stars/valeriogalano/pensieriincodice-cdn?style=for-the-badge" alt="GitHub Stars"/>
    <img src="https://img.shields.io/github/forks/valeriogalano/pensieriincodice-cdn?style=for-the-badge" alt="GitHub Forks"/>
    <img src="https://img.shields.io/github/last-commit/valeriogalano/pensieriincodice-cdn?style=for-the-badge" alt="Last Commit"/>
    <a href="https://pensieriincodice.it/sostieni" target="_blank" rel="noopener noreferrer">
      <img src="https://img.shields.io/badge/sostieni-Pensieri_in_codice-fb6400?style=for-the-badge" alt="Sostieni Pensieri in codice"/>
    </a>
  </p>
</div>

---

## Indice

- [Come funziona](#come-funziona)
- [Struttura della repository](#struttura-della-repository)
- [Requisiti](#requisiti)
- [Generazione trascrizioni](#generazione-trascrizioni)
- [Aggiunta capitoli](#aggiunta-capitoli)
- [Aggiunta cover](#aggiunta-cover)
- [Tag ID3 per gli MP3](#tag-id3-per-gli-mp3)
- [Contributi](#contributi)
- [Importante](#importante)

---

## Come funziona

Questa repository funge da punto centralizzato e versionato per tutte le risorse statiche del podcast. Grazie ad alcune GitHub Actions sono state aggiunte automazioni per facilitare le fasi del processo di produzione (conversione capitoli, generazione cover, tagging ID3).

---

## Struttura della repository

```
/
├── .github/
│   └── workflows/                  # GitHub Actions
│
├── public/
│   ├── chapters/                   # File JSON con i capitoli degli episodi
│   ├── covers/                     # Locandine episodi definitive
│   ├── episodes/                   # File MP3 degli episodi
│   ├── images/                     # Immagini varie
│   └── transcripts/                # Trascrizioni episodi (.srt)
│
├── raw/
│   ├── chapters/                   # File .txt con i capitoli (input)
│   └── covers/                     # Locandine da elaborare (input)
│
├── utils/
│   ├── chapters_converter/         # Converte capitoli da .txt a .json
│   ├── cover_formatter/            # Formatta le cover (usato anche dalla GitHub Action)
│   ├── id3_tagger/                 # Aggiunge tag ID3 agli MP3
│   └── transcripts_generator/      # Genera trascrizioni con whisper.cpp
│       └── models/                 # Modelli scaricati al primo avvio
│
└── README.md
```

---

## Requisiti

| Strumento | Utilizzo |
|---|---|
| `ffmpeg` | Conversione audio per le trascrizioni |
| `whisper` (binario whisper.cpp) | Generazione trascrizioni |
| `curl` | Download del modello al primo avvio |
| PHP 5.6+ | Conversione capitoli da .txt a .json |
| Python 3.9+ | Formattazione cover e tagging ID3 |
| `pngquant` (opzionale) | Ottimizzazione PNG delle cover |
| `mutagen` (pip) | Tagging ID3 degli MP3 |

### Installazione ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg
```

---

## Generazione trascrizioni

Le trascrizioni vengono generate tramite `utils/transcripts_generator/transcripts_generator.sh`, che usa `whisper.cpp`. Lo script legge i file `.mp3` in `public/episodes/` e genera i corrispondenti `.srt` in `public/transcripts/`, saltando quelli già presenti.

### Installazione del binario whisper

**Opzione A — binario precompilato:** scarica un binario dalla pagina release di whisper.cpp, rinominalo `whisper`, copialo in `utils/` e rendilo eseguibile:

```bash
chmod +x utils/whisper
```

**Opzione B — compilazione da sorgente:**

```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp && make
cp main ../utils/whisper && chmod +x ../utils/whisper
```

### Esecuzione

```bash
cd utils/transcripts_generator

# Genera tutte le trascrizioni mancanti
./transcripts_generator.sh

# Genera solo per un episodio specifico
./transcripts_generator.sh PIC123
```

Alla prima esecuzione viene scaricato automaticamente il modello `ggml-large-v3` in `models/`.

### Troubleshooting

| Errore | Soluzione |
|---|---|
| `permission denied` | `chmod +x utils/transcripts_generator/transcripts_generator.sh utils/whisper` |
| `./whisper: file o directory non esistente` | Verifica che il binario si chiami `whisper` e si trovi in `utils/` |
| `ffmpeg` non trovato | Installalo e riapri il terminale |
| Errore download modello | Verifica la connessione e riprova |

---

## Aggiunta capitoli

I file di input vanno in `raw/chapters/` con nome `<numero_episodio>.txt`. Il formato di ogni riga è:

```
<start> <end> <titolo> [URL opzionale]
```

Esempi:

```
0.000000 168.000000 Intro
924.312130 924.312130 Sito web https://pensieriincodice.it
260.000000 300.000000 Sezione immagine https://example.com/cover.png
```

Se la riga contiene un URL a un'immagine (`.jpg`, `.png`, `.gif`, `.webp`, `.svg`), viene inserito nel campo `img`; altrimenti nel campo `url`. L'URL viene rimosso dal testo del titolo.

### Conversione in locale

```bash
# Conversione standard (salta gli episodi già convertiti)
php utils/chapters_converter/chapters_converter.php

# Forza la rigenerazione di tutti i JSON
php utils/chapters_converter/chapters_converter.php --force
```

I file JSON vengono creati in `public/chapters/PIC{EPISODIO}.json`. Per rigenerare un episodio già convertito, elimina prima il file JSON corrispondente.

### Struttura del JSON generato

```json
{
  "version": "1.2.0",
  "chapters": [
    { "startTime": 0, "title": "Intro" },
    { "startTime": 924.31213, "title": "Sito web", "url": "https://pensieriincodice.it" },
    { "startTime": 260, "title": "Sezione immagine", "img": "https://example.com/cover.png" }
  ]
}
```

---

## Aggiunta cover

Le cover di input vanno in `raw/covers/` con la seguente nomenclatura:

| File | Descrizione |
|---|---|
| `<numero>.png` | Cover standard dell'episodio |
| `<numero>-ce.png` | Cover Community Edition dell'episodio |

Esempio: `145.png`, `145-ce.png`.

### Generazione in locale

```bash
cd utils/cover_formatter
pip install -r requirements.txt

# Generazione standard
python main.py --images_dir ../../raw/covers

# Con font personalizzato (da URL)
python main.py --images_dir ../../raw/covers \
  --font_url "https://raw.githubusercontent.com/valeriogalano/pensieriincodice-assets/refs/heads/main/fonts/Courier%2010%20Pitch%20Regular.otf"

# Con font personalizzato (locale)
python main.py --images_dir ../../raw/covers \
  --font_path "/percorso/al/font/Courier 10 Pitch Regular.otf"
```

Le cover finali vengono scritte in `public/covers/PIC{EPISODIO}.png`. Le cover già presenti vengono saltate.

---

## Tag ID3 per gli MP3

Lo script aggiunge automaticamente i tag ID3v2 ai file MP3 privi di tag, impostando titolo, artista, album, genere e commento. I file già taggati vengono saltati.

### Esecuzione

```bash
# Installazione dipendenza
pip install mutagen

# Tagging standard
python3 utils/id3_tagger/id3_tagger.py --audio_dir public/episodes

# Con cover (stessa immagine per tutti i file elaborati)
python3 utils/id3_tagger/id3_tagger.py \
  --audio_dir public/episodes \
  --cover public/covers/PIC145.png
```

### Troubleshooting

| Errore | Soluzione |
|---|---|
| `ModuleNotFoundError: No module named 'mutagen'` | `pip install mutagen` |
| Permessi negati | Verifica che i file non siano aperti da altri programmi |
| Cover non incorporata | Usa un file `.png` esistente e verifica il percorso |

---

## Repository correlati

- [pensieriincodice-assets](https://github.com/valeriogalano/pensieriincodice-assets) — Sorgenti degli asset (frame, font, audio)
- [pensieriincodice-website](https://github.com/valeriogalano/pensieriincodice-website) — Sito web Hugo del podcast

---

## Contributi

Se noti qualche problema o hai suggerimenti, sentiti libero di aprire una **Issue** e successivamente una **Pull Request**. Ogni contributo è ben accetto!

---

## Importante

Vorremmo mantenere questo repository aperto e gratuito per tutti, ma lo scraping del contenuto di questo repository **NON È CONSENTITO**. Se ritieni che questo lavoro ti sia utile e vuoi utilizzare qualche risorsa, ti preghiamo di citare come fonte il podcast e/o questo repository.

---

<div align="center">
  <p>Realizzato con ❤️ da <strong>Valerio Galano</strong></p>
  <p>
    <a href="https://valeriogalano.it/">Sito Web</a> |
    <a href="https://daredevel.com/">Blog</a> |
    <a href="https://pensieriincodice.it/">Podcast</a> |
    <a href="https://www.linkedin.com/in/valeriogalano/">LinkedIn</a>
  </p>
</div>
