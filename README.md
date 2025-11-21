<div align="center">
  <img src="https://raw.githubusercontent.com/valeriogalano/pensieriincodice-assets/main/images/pensieriincodice-2-logo-telegram.png" alt="Logo Progetto" width="150"/>
  <h1>Pensieri In Codice - CDN</h1>
  <p>
    Una repository Content Delivery Network (CDN) per ospitare e servire asset statici come immagini, audio e altri file per il podcast <a href="https://pensieriincodice.it/">pensieriincodice.it</a>.
  </p>
  
  <p>
    <img src="https://img.shields.io/github/stars/valeriogalano/pensieriincodice-cdn?style=for-the-badge" alt="GitHub Stars"/>
    <img src="https://img.shields.io/github/forks/valeriogalano/pensieriincodice-cdn?style=for-the-badge" alt="GitHub Forks"/>
    <img src="https://img.shields.io/github/last-commit/valeriogalano/pensieriincodice-cdn?style=for-the-badge" alt="Last Commit"/>
    <a href="https://www.satispay.com/download/qrcode/S6Y-CON--EC548199-5F32-4BD6-AAF5-73A999744E56" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/dona con-Satispay-E62E1A?style=for-the-badge&logo=satispay&logoColor=white" alt="Dona con Satispay"></a>
    <a href="https://www.paypal.com/donate/?hosted_button_id=HRKMD7X43R7SS" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/dona con-Paypal-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="Dona con Paypal"></a>
  </p>
</div>

---

## Scopo del Progetto

Questa repository funge da **CDN** per il podcast di [Pensieri in Codice](https://pensieriincodice.it/)
un podcast a cura di [Valerio Galano](https://valeriogalano.it/). 

L'obiettivo è di avere un unico punto centralizzato e versionato per la gestione di tutte le risorse statiche 
(loghi, locandine, episodi, trascrizioni ecc.).

Grazie ad alcune GitHub actions sono state aggiunte delle automazioni
per facilitare alcune fasi del processo di sviluppo.

---

## Struttura della Repository

La repository è organizzata in cartelle per mantenere l'ordine e facilitare la ricerca dei file.

```
/
├── .github/
│   ├── workflows/                  # GitHub actions
│
├── public/
│   ├── chapters/                  # file json con i capitoli degli episodi
│   ├── covers/                    # locandine episodi definitive
│   ├── episodes/                  # file mp3 degli episodi
│   ├── images/                    # per le immagini
│   ├── transcripts/               # trascrizioni episodi
│   └── video/                     # per i video
│
├── raw/
│   ├── chapters/                  # file txt con i capitoli degli episodi
│   └── covers/                    # locandine degli episodi da elaborare
│
├── utils/
│   ├── audio/                     # strumenti audio (es. ID3 tagger)
│   ├── chapters/                  # strumenti per i capitoli (txt -> json)
│   ├── covers/                    # utility per cover (script locali)
│   ├── transcripts/               # strumenti per generare trascrizioni
│   ├── models/                    # modelli per whisper.cpp (scaricati al primo avvio)
│   └── cover_formatter/           # usato nella GitHub action
│
└── README.md                      # questo file

```

## Generare i capitoli (txt → json) in locale

Questo progetto include uno script PHP che converte i file di capitoli in formato testo in file JSON compatibili con il player. Lo script rileva automaticamente eventuali URL presenti nelle righe dei capitoli e li inserisce nel JSON.

### Requisiti
- PHP 5.6 o superiore (consigliato). Funziona anche con versioni precedenti purché `json_encode` sia disponibile.

### Dove mettere i file di input
- Capitoli: `raw/chapters/{EPISODIO}.txt`
  - Formato di ogni riga: `start end titolo [URL]`
  - Esempi:
    - `0.000000 168.000000 Intro`
    - `924.312130 924.312130 Link al sito https://pensieriincodice.it` → aggiunge `url` al capitolo
    - `168.000000 260.000000 Sezione con immagine https://example.com/cover.png` → aggiunge `img` al capitolo

Note sul parsing URL:
- Lo script cerca il primo URL `http://` o `https://` presente nella riga (in qualunque posizione dopo i tempi).
- Se l'URL punta a un'immagine (`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`), viene inserito nel campo `img`.
- Negli altri casi viene inserito nel campo `url`.
- L'URL, se presente, viene rimosso dal testo del titolo.
- Se la riga contiene solo un link o solo un'immagine (cioè nessun altro testo oltre agli URL), il campo `title` viene omesso.

Nota: `{EPISODIO}` è il numero dell'episodio (es. `145`).

### Output generato
- I JSON vengono creati in `public/chapters/` con nome `PIC{EPISODIO}.json` (es. `public/chapters/PIC145.json`).

### Come eseguire lo script
Dal root della repo:

```bash
php utils/chapters/convert_chapters.php
```

Opzioni utili:

- `--force`: forza la rigenerazione anche se il JSON di output esiste già.

Esempi:

```bash
# conversione standard (salta gli episodi già convertiti)
php utils/chapters/convert_chapters.php

# forza la rigenerazione di tutti i JSON
php utils/chapters/convert_chapters.php --force
```

Lo script:
- scansiona `raw/chapters/` per tutti i file `.txt`;
- per ogni riga, estrae `startTime`, `title` e, se presente, un URL (come `url` o `img` a seconda dell'estensione);
- ordina i capitoli per `startTime` e salva in `public/chapters/PIC{EPISODIO}.json`.

### Rigenerare un episodio già convertito
Per evitare lavoro inutile, lo script salta i file la cui uscita JSON è già presente. Se modifichi i capitoli o aggiungi dei link e vuoi rigenerare il JSON:

1. elimina il file `public/chapters/PIC{EPISODIO}.json` relativo;
2. rilancia il comando:
   ```bash
   php utils/chapters/convert_chapters.php
   ```

### Esempio pratico
Con il file `raw/chapters/145.txt` contenente una riga:

```
924.312130 924.312130 Qualche esempio https://pensieriincodice.it
```

il JSON `public/chapters/PIC145.json` conterrà, alla posizione `924.31213`, un capitolo con `title: "Qualche esempio"` e `url: "https://pensieriincodice.it"`.

E se la riga fosse:

```
260.000000 300.000000 Sezione immagine https://example.com/img.png
```

nel capitolo verrebbe aggiunto `"img": "https://example.com/img.png"` al posto di `url`.

### Messaggi a console
Durante l'esecuzione vedrai righe come:
- `Converting raw/chapters/145.txt` quando un episodio viene elaborato
- `Skipping raw/chapters/129.txt (output exists)` quando il relativo JSON esiste già

### Struttura del JSON
Ogni file generato ha la forma:

```json
{
  "version": "1.2.0",
  "chapters": [
    { "startTime": 0, "title": "Intro" },
    { "startTime": 924.31213, "title": "Qualche esempio", "url": "https://pensieriincodice.it" },
    { "startTime": 260, "title": "Sezione immagine", "img": "https://example.com/img.png" },
    { "startTime": 724.31213, "img": "https://example.com/only-image.png" },
    { "startTime": 1024.5, "url": "https://example.com/only-link" }
  ]
}
```

## Aggiunta di nuovi contenuti

### Aggiunta capitoli

I file con i capitoli degli episodi vanno posizionati nella cartella `raw/chapters/` con la seguente nomenclatura:

- **Nome file**: `<numero_episodio>.txt`
- **Esempio**: `145.txt` per l'episodio 145

Il file verrà automaticamente elaborato e convertito in formato JSON nella cartella `public/chapters/`.

### Aggiunta cover

Le cover degli episodi vanno posizionate nella cartella `raw/covers/` con la seguente nomenclatura:

- **Cover standard**: `<numero_episodio>.png`
- **Cover Community Edition**: `<numero_episodio>-ce.png`

**Esempi**:
- `145.png` per la cover standard dell'episodio 145
- `145-ce.png` per la cover Community Edition dell'episodio 145

Il suffisso `-ce` serve per distinguere le cover degli episodi Community Edition che differiscono da quelle regolari. I file verranno automaticamente elaborati e copiati nella cartella `public/covers/`.

---

## Utilizzo locale: generazione trascrizioni con shell (whisper.cpp)

Prima opzione (consigliata per velocità/zero dipendenze Python): usa lo script `utils/transcripts/generate_transcripts.sh`, che sfrutta `whisper.cpp`.

- Come funziona: legge i file `.mp3` in `public/episodes` e crea (se mancanti) i corrispondenti `.srt` in `public/transcripts`.
- Modello usato: `ggml-large-v3` (italiano). Gli `.srt` esistenti vengono lasciati intatti.
- Il modello viene scaricato automaticamente nella prima esecuzione in `utils/models/`.

### Requisiti
- `ffmpeg` installato nel sistema
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
- `curl` (per scaricare il modello al primo avvio)
- Un binario `whisper` di `whisper.cpp` posizionato nella cartella `utils/`
  - Opzione A (precompilato): scarica un binario dalla pagina release di whisper.cpp e rinominalo in `whisper`, poi mettilo in `utils/` e rendilo eseguibile: `chmod +x utils/whisper`
  - Opzione B (compilazione):
    - `git clone https://github.com/ggerganov/whisper.cpp`
    - `cd whisper.cpp && make` (richiede un toolchain C/C++; su macOS `xcode-select --install`, su Ubuntu `sudo apt install build-essential`)
    - copia il binario prodotto (`main`) in `utils/` e rinominalo `whisper`: `cp main ../utils/whisper && chmod +x ../utils/whisper`

### Preparazione dei file
- Copia gli episodi `.mp3` nella cartella `public/episodes`.
- La cartella `public/transcripts` verrà creata automaticamente se assente.

### Esecuzione
Esegui dalla cartella `utils/transcripts` (lo script usa percorsi relativi alla sua posizione):

```bash
cd utils/transcripts
./generate_transcripts.sh            # genera tutte le trascrizioni mancanti
./generate_transcripts.sh PIC123     # genera solo per lo specifico episodio PIC123.mp3
```

Output atteso:
- Alla prima esecuzione scarica `models/ggml-large-v3.bin`.
- Converte temporaneamente gli MP3 in WAV, invoca `./whisper` e scrive gli `.srt` in `public/transcripts/`.
- Non sovrascrive trascrizioni già presenti.

### Troubleshooting
- `permission denied`: esegui `chmod +x utils/transcripts/generate_transcripts.sh utils/whisper`.
- `./whisper: file o directory non esistente`: assicurati che il binario si chiami `whisper` e sia in `utils/`.
- `ffmpeg` non trovato: installalo e riapri il terminale.
- Errori di download del modello: verifica la connessione o riprova più tardi.

---

## Alternativa: generazione trascrizioni in Python (OpenAI Whisper)

Puoi anche generare i file di trascrizione `.srt` usando lo script `utils/transcripts/generate_transcripts.py`, che sfrutta OpenAI Whisper.

- Come funziona: legge i file `.mp3` in `public/episodes` e crea (se mancanti) i corrispondenti `.srt` in `public/transcripts`.
- Modello usato: `base` (italiano). Gli `.srt` esistenti vengono lasciati intatti.

### Requisiti
- Python 3.9+ (consigliato 3.10/3.11)
- `ffmpeg` installato nel sistema (necessario per Whisper)
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
  - Windows: scarica da https://www.gyan.dev/ffmpeg/ e aggiungi `ffmpeg` al PATH

### Installazione dipendenze
Esegui i comandi dalla root del progetto.

```bash
# (opzionale) crea e attiva un virtualenv
python3 -m venv .venv
source .venv/bin/activate   # su Windows: .venv\Scripts\activate

# installa le dipendenze
pip install -r requirements.txt

# se Whisper non fosse presente nel requirements.txt, installalo così:
# pip install openai-whisper
```

Nota: Whisper installerà anche PyTorch. Se disponi di GPU, verrà usata automaticamente quando supportata (CUDA su NVIDIA, MPS su Apple Silicon con versioni recenti di PyTorch).

### Preparazione dei file
- Copia gli episodi `.mp3` nella cartella `public/episodes`.
- Assicurati che la cartella `public/transcripts` esista; in caso contrario verrà creata dallo script.

### Esecuzione
Esegui lo script dalla root del repository (importante: usa la root perché lo script imposta percorsi relativi `./public/...`).

```bash
python utils/transcripts/generate_transcripts.py
```

Output atteso:
- Per ogni `*.mp3` in `public/episodes`, se non esiste già, viene creato `public/transcripts/<nomefile>.srt`.
- Log a console con lo stato della trascrizione e i file creati.

### Troubleshooting
- Errore su `ffmpeg` non trovato: installa `ffmpeg` e riapri il terminale.
- Prestazioni lente: su CPU può richiedere tempo; usa un modello più piccolo (ad es. `tiny`/`small`) o una macchina con GPU.
- Apple Silicon: con versioni recenti di PyTorch, l'accelerazione MPS è automatica; aggiorna PyTorch se non viene rilevata.

---

## Contributi

Se noti qualche problema o hai suggerimenti per migliorare l'organizzazione, sentiti libero di aprire una **Issue**
e successivamente una **Pull Request**. Ogni contributo è ben accetto!

---

## Importante

Vorremmo mantenere questo repository aperto e gratuito per tutti,
ma lo scraping del contenuto di questo repository NON È CONSENTITO.
Se ritieni che questo lavoro ti sia utile e vuoi utilizzare qualche risorsa,
ti preghiamo di citare come fonte il podcast e/o questo repository.

---

<div align="center">
  <p>
    Realizzato con ❤️ da <strong>Valerio Galano</strong>
  </p>
  <p>
    <a href="https://valeriogalano.it/">Sito Web</a> | 
    <a href="https://daredevel.com/">Blog</a> | 
    <a href="https://pensieriincodice.it/">Podcast</a> | 
    <a href="https://www.linkedin.com/in/valeriogalano/">LinkedIn</a>
  </p>
</div>