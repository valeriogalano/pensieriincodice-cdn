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