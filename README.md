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
│   └── workflows/                  # GitHub actions
│
├── public/
│   ├── chapters/                  # file json con i capitoli degli episodi
│   ├── covers/                    # locandine episodi definitive
│   ├── episodes/                  # file mp3 degli episodi
│   ├── images/                    # per le immagini
│   └── transcripts/               # trascrizioni episodi
│
├── raw/
│   ├── chapters/                  # file txt con i capitoli degli episodi
│   └── covers/                    # locandine degli episodi da elaborare
│
├── utils/
│   ├── chapters/                  # strumenti per i capitoli (txt -> json)
│   ├── cover_formatter/           # usato nella GitHub action
│   ├── id3_tagger/                # strumenti audio (es. ID3 tagger)
│   └── transcripts/               # strumenti per generare trascrizioni
│       └── models/                # modelli per whisper.cpp (scaricati al primo avvio)
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
php utils/chapters_converter/chapters_converter.php
```

Opzioni utili:

- `--force`: forza la rigenerazione anche se il JSON di output esiste già.

Esempi:

```bash
# conversione standard (salta gli episodi già convertiti)
php utils/chapters_converter/chapters_converter.php

# forza la rigenerazione di tutti i JSON
php utils/chapters_converter/chapters_converter.php --force
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
   php utils/chapters_converter/chapters_converter.php
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

### Generare le cover (in locale)

Per generare le cover finali con il frame e il numero episodio, è disponibile uno script Python in `utils/cover_formatter`.

#### Requisiti
- Python 3.9+ (consigliato 3.10/3.11)
- `pip` per installare le dipendenze
- Connessione Internet (lo script scarica automaticamente il frame dal repository degli asset)
- Opzionale: `pngquant` per ottimizzare i PNG finali
  - macOS: `brew install pngquant`
  - Ubuntu/Debian: `sudo apt update && sudo apt install pngquant`

Le dipendenze Python specifiche del tool sono elencate in `utils/cover_formatter/requirements.txt` (include OpenCV e NumPy).

#### Installazione dipendenze (una tantum)
Esegui dalla cartella del formatter:

```bash
cd utils/cover_formatter

# (opzionale) ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate   # su Windows: .venv\Scripts\activate

# installa le dipendenze del formatter
pip install -r requirements.txt
```

#### Preparazione input
Metti le immagini sorgenti in `raw/covers/`. Sono accettati file `.png` o `.jpg` con questi nomi comuni:
- `145.png` → episodio 145
- `PIC145.png` → episodio 145
- `145-ce.png` → episodio 145, tag `ce` (Community Edition)
- `PIC145-ce.jpg` → episodio 145, tag `ce`

Lo script rileva automaticamente:
- il numero dell’episodio dal nome file (verrà scritto in alto a sinistra sulla cover);
- il “tag” dopo il trattino (es. `-ce`) per selezionare il frame corretto.

#### Esecuzione
Lancia lo script dalla cartella `utils/cover_formatter` specificando la cartella delle immagini di input:

```bash
cd utils/cover_formatter
python main.py --images_dir ../../raw/covers
```

Output atteso:
- Le cover finali vengono scritte in `public/covers/` con nome `PIC{EPISODIO}.png` (es. `public/covers/PIC145.png`).
- Se `pngquant` è presente, i PNG vengono ottimizzati automaticamente.
- Le cover già presenti in `public/covers/` vengono saltate (non vengono rigenerate).

Note:
- Esegui lo script dalla cartella `utils/cover_formatter` perché usa percorsi relativi per la cartella di output (`../../public/covers`).
- Il numero episodio viene disegnato solo se nel nome file è presente almeno una cifra.
- Il frame appropriato viene scaricato in base al tag del filename: ad esempio `145-ce.png` userà `frame-ce.png`.

## Aggiungere tag ID3 agli MP3 (uso locale)

Questo repository include uno script Python per aggiungere automaticamente i tag ID3v2 ai file MP3 degli episodi che ne sono sprovvisti.

### Dove si trova
- Script: `utils/id3_tagger/id3_tagger.py`

### Cosa fa
- Legge tutti i file `*.mp3` in una cartella specificata con `--audio_dir`.
- Se un file ha già tag ID3, lo salta automaticamente.
- Per i file senza tag, imposta i campi principali con valori predefiniti:
  - `Title (TIT2)`: "Episodio {NUMERO}" (il numero è estratto dal nome file, es. `PIC145.mp3` → 145). Se il numero non è reperibile, usa il nome file.
  - `Artist (TPE1)`: "Valerio Galano"
  - `Album (TALB)`: "Pensieri in codice"
  - `Album Artist (TPE2)`: "Valerio Galano"
  - `Genre (TCON)`: "Technology"
  - `Comment (COMM)`: "Il podcast dove si ragiona da informatici" (lingua `ita`)
- Opzionalmente incorpora una cover (fronte) se fornita con l’opzione `--cover`.

### Requisiti
- Python 3.8+
- `pip` per installare le dipendenze

Installa la dipendenza necessaria (una tantum):

```bash
pip install mutagen
```

Se usi un ambiente virtuale:

```bash
python3 -m venv .venv
source .venv/bin/activate   # su Windows: .venv\Scripts\activate
pip install mutagen
```

### Preparazione file
- Metti gli MP3 degli episodi in `public/episodes` (o in un’altra cartella a tua scelta) con una nomenclatura tipo `PIC145.mp3`, `PIC146.mp3`, ecc.
- Se vuoi incorporare una cover, prepara un file PNG della cover dell’episodio.
  - Nota: lo script imposta `mime='image/png'`, quindi usa preferibilmente cover in formato PNG.

### Esecuzione
Esegui dal root della repo specificando la cartella con gli MP3:

```bash
python3 utils/audio/id3_tagger.py --audio_dir public/episodes
```

Con cover (stessa cover per tutti i file elaborati in quella run):

```bash
python3 utils/audio/id3_tagger.py \
  --audio_dir public/episodes \
  --cover public/covers/PIC145.png
```

Esempio con una cartella temporanea:

```bash
python3 utils/audio/id3_tagger.py --audio_dir /percorso/ai/tuoi/mp3
```

Output a console tipico:
- `Skipping PIC145.mp3 (already has ID3 tags)` → file già taggato, saltato
- `Adding ID3 tags to PIC146.mp3...` → tag aggiunti
- Al termine stampa un riepilogo con `Processed`, `Skipped`, `Failed`.

### Note e limitazioni
- Estrazione numero episodio: avviene cercando le cifre nel nome file (es. `PIC123.mp3` → 123). Se non trova numeri, il titolo sarà il nome file.
- Cover: l’opzione `--cover` applica la stessa immagine a tutti i file processati in quella esecuzione.
- Lo script aggiunge i tag solo ai file che risultano privi di tag ID3; non sovrascrive tag esistenti.

### Troubleshooting
- Errore `ModuleNotFoundError: No module named 'mutagen'`:
  - Soluzione: installa la dipendenza con `pip install mutagen` (nell’ambiente corretto).
- Permessi negati o file in uso:
  - Assicurati che i file MP3 non siano aperti da altri programmi e di avere permessi di scrittura nella cartella.
- Cover non incorporata:
  - Verifica il percorso passato a `--cover` e usa un file `.png` esistente.

## Generazione trascrizioni (in locale)

Prima opzione (consigliata per velocità/zero dipendenze Python): usa lo script `utils/transcripts_generator/transcripts_generator.sh`, che sfrutta `whisper.cpp`.

- Come funziona: legge i file `.mp3` in `public/episodes` e crea (se mancanti) i corrispondenti `.srt` in `public/transcripts`.
- Modello usato: `ggml-large-v3` (italiano). Gli `.srt` esistenti vengono lasciati intatti.
- Il modello viene scaricato automaticamente nella prima esecuzione in `utils/transcripts_generator/models/`.

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
Esegui dalla cartella `utils/transcripts_generator` (lo script usa percorsi relativi alla sua posizione):

```bash
cd utils/transcripts_generator
./transcripts_generator.sh            # genera tutte le trascrizioni mancanti
./transcripts_generator.sh PIC123     # genera solo per lo specifico episodio PIC123.mp3
```

Output atteso:
- Alla prima esecuzione scarica `models/ggml-large-v3.bin`.
- Converte temporaneamente gli MP3 in WAV, invoca `./whisper` e scrive gli `.srt` in `public/transcripts/`.
- Non sovrascrive trascrizioni già presenti.

### Troubleshooting
- `permission denied`: esegui `chmod +x utils/transcripts_generator/transcripts_generator.sh utils/whisper`.
- `./whisper: file o directory non esistente`: assicurati che il binario si chiami `whisper` e sia in `utils/`.
- `ffmpeg` non trovato: installalo e riapri il terminale.
- Errori di download del modello: verifica la connessione o riprova più tardi.

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