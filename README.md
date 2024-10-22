# Progetti Python

Questa repository contiene diversi progetti Python che coprono varie aree di applicazione.

## 1. Generative AI Web Application

Un'applicazione web per interagire con l'API Generative AI di Google (Gemini).

### Funzionalità
- Creare favole
- Rispondere a domande testuali
- Analizzare immagini e rispondere a domande su di esse

### File principali
- `server.py`: Server Flask per l'applicazione web e gestione delle richieste API
- `client.py`: Modulo per l'interazione con l'API di Google Gemini
- `index.html`: Pagina HTML principale per l'interfaccia utente
- `script.js`: JavaScript per la logica dell'interfaccia utente
- `style.css`: Foglio di stile CSS per l'interfaccia utente

### Struttura del progetto
- `/`: Contiene i file principali del server e del client
- `/templates`: Contiene i file HTML per il frontend
- `/static`: Contiene i file JS e CSS per il frontend
- `/uploads`: Directory per le immagini caricate dagli utenti

### Caratteristiche principali
- Interfaccia web responsive con Flask
- Caricamento e analisi di immagini direttamente dal browser
- Visualizzazione dei risultati con scrolling assistito
- Gestione dinamica del form basata sulla selezione dell'utente
- Integrazione seamless con l'API di Google Gemini

## 2. Server HTTP Flask

Un'applicazione web basic basata su Flask.

### Funzionalità
- Registrazione utenti
- Pagine di conferma registrazione

### File principali
- `server.py`
- Templates HTML in `/templates`

## 3. API REST

Un'API REST per la gestione di dati anagrafici.

### Funzionalità
- CRUD operations su dati cittadini
- Autenticazione basica

### File principali
- `server.py` (API)
- `client.py` (client di test)

## 4. Sniffer di Rete

Uno strumento per l'analisi del traffico di rete.

### Funzionalità
- Cattura e analisi di pacchetti
- Supporto per protocolli HTTP

### File principali
- `sniff.py`

## 5. Cerca Stringa

Uno script per cercare stringhe in file e directory.

### Funzionalità
- Ricerca ricorsiva in directory
- Supporto per vari tipi di file (testo, PDF, DOC)

### File principali
- `cerca.py`


