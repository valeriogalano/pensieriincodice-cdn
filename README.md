<div align="center">
  <img src="https://raw.githubusercontent.com/valeriogalano/pensieriincodice-assets/main/images/pensieriincodice-logo-telegram-community.png" alt="Logo Progetto" width="150"/>
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
│   └── cover_formatter/           # usato nella GitHub action
│
└── README.md                      # questo file
```

## Utilizzo locale: generazione trascrizioni in Python (Whisper)

Puoi generare in locale i file di trascrizione `.srt` degli episodi usando lo script `utils/generate_transcripts.py`, che sfrutta OpenAI Whisper.

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
python utils/generate_transcripts.py
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