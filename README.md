# Progetti Python

Questa repository contiene diversi progetti Python che coprono varie aree di applicazione.

## 1. Generative AI Client

Un client per interagire con l'API Generative AI di Google (Gemini).

### Funzionalità
- Creare favole
- Rispondere a domande testuali
- Analizzare immagini

### File principali
- `client.py`: Client principale per interagire con l'API
- `myjson.py`: Funzioni per gestire operazioni JSON
- `creajsonpersf.sh`: Script Bash per creare JSON per richieste di immagini
- `server.py`: Server Flask per l'interfaccia web
- `index.html`: Pagina HTML principale per l'interfaccia utente
- `script.js`: JavaScript per la logica dell'interfaccia utente
- `style.css`: Foglio di stile CSS per l'interfaccia utente

### Struttura del progetto
- `/api`: Contiene i file Python per il backend
- `/public`: Contiene i file HTML per il frontend
- `/src`: Contiene i file JS e CSS per il frontend

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

## Requisiti generali

- Python 3.x
- Varie librerie Python (vedi `requirements.txt` in ogni progetto)
- Un ambiente di sviluppo Python (ad esempio, `virtualenv`)

