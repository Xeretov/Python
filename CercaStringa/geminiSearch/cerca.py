import os
from geminiSearch import search

def ricerca_per_nome(file_path: str, stringa: str) -> bool:
    """
    Cerca la stringa nel nome del file
    """
    nome_file = os.path.basename(file_path).lower()
    return stringa.lower() in nome_file

def ricerca_contenuti(file_path: str, stringa: str, tipo: int) -> tuple[bool, str]:
    '''
    Analizza il contenuto di un file usando Gemini e cerca la stringa specificata.
    file_type: 1 per PDF, 2 per DOCX, 3 per immagini
    '''
    try:
        result: str = search(tipo, file_path)
        return stringa.lower() in result.lower(), result
    except Exception as e:
        print(f"Errore nell'analisi del file {file_path}: {str(e)}")
        return False, ""

def ricerca_file(root_dir: str, stringa: str) -> tuple[list, list, list]:

    risultati_testo = []
    risultati_immagine = []
    risultati_nome = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            # Ricerca del nome del file
            if ricerca_per_nome(file_path, stringa):
                risultati_nome.append(file_path)

            try:
                if ext == '.pdf':
                    trovato, contenuto = ricerca_contenuti(file_path, stringa, 1)
                    if trovato:
                        risultati_testo.append((file_path, contenuto, "PDF"))
                elif ext in ['.doc','.docx']:
                    trovato, contenuto = ricerca_contenuti(file_path, stringa, 2)
                    if trovato:
                        risultati_testo.append((file_path, contenuto, "DOCX"))
                elif ext in ['.jpg','.jpeg','.png']:
                    trovato, descrizione = ricerca_contenuti(file_path, stringa, 3)
                    if trovato:
                        risultati_immagine.append((file_path, descrizione))
                elif ext == '.txt':
                    try:
                        with open(file_path, 'r') as f:
                            contenuto = f.read().lower()
                            if stringa.lower() in contenuto:
                                risultati_testo.append((file_path, contenuto, "TXT"))
                    except:
                        print(f"Errore nella lettura del file: {file_path}")
            except Exception as e:
                print(f"Errore nel processare {file_path}: {str(e)}")
                continue
    return  risultati_testo, risultati_immagine, risultati_nome

def stampa_risultati(risultati_testo, risultati_immagini, risultati_nome, stringa, modo="console", file_output=None) -> None:
    """
    Stampa i risultati in base alla modalità specificata
    modo: "console", "file" o "entrambe"
    default:
    -modo = "console"
    -file_output = None
    """
    def stampa_messaggio(messaggio, file=None):
        if modo in ["console","entrambe"]:
            print(messaggio)
        if modo in ["file","entrambe"] and file:
            file.write(messaggio + "\n")

    # Apre il file di output se necessario
    file = None
    if modo in ["file","entrambe"]:
        if not file_output:
            file_output = "risultati_ricerca.txt"
        file = open(file_output, "a", encoding="utf-8")
    
    # Stampa risultati per i nomi dei file
    stampa_messaggio(f"\nLa stringa '{stringa}' è stata trovata nel nome di {len(risultati_nome)} file.", file)
    if risultati_nome:
        stampa_messaggio("\nFile con nome contenente la stringa:", file)
        for file_path in risultati_nome:
            stampa_messaggio(f"- {file_path}", file)
    
    # Stampa risultati per i file di testo
    stampa_messaggio(f"\nLa stringa '{stringa}' è stata trovata nel contenuto di {len(risultati_testo)} file di testo.", file)
    if risultati_testo:
        stampa_messaggio("\nFile contenenti la stringa:", file)
        for file_path, contenuto, tipo in risultati_testo:
            messaggio = f"\nFile: {file_path}\nTipo: {tipo}\nContenuto: {contenuto[:100]}...\n" if len(contenuto) > 100 else f"\nFile: {file_path}\nTipo: {tipo}\nContenuto: {contenuto}\n"
            stampa_messaggio(messaggio, file)

    # Stampa risultati per le immagini
    stampa_messaggio(f"\nLa stringa '{stringa}' è stata trovata nella descrizione  di {len(risultati_immagini)} immagini.", file)
    if risultati_immagini:
        stampa_messaggio("\nImmagini con descrizione contenente la stringa:", file)
        for file_path, descrizione in risultati_immagini:
            messaggio = f"\nImmagine: {file_path}\nDescrizione: {descrizione[:100]}...\n" if len(descrizione) > 100 else f"\nImmagine: {file_path}\nDescrizione: {descrizione}\n"
            stampa_messaggio(messaggio, file)

    if file:
        file.close()

def preparazione_file_output(nome_file):
    """
    Controlla se il nome del file inserito sia corretto o se esiste già
    """
    if not nome_file:
        nome_file = "risultati_ricerca.txt"
    # Aggiungi estensione .txt se mancante
    if not nome_file.lower().endswith('.txt'):
        nome_file += '.txt'
    
    # Gestione file esistente
    cont = 1
    nome_base = nome_file[:-4] # rimuove .txt
    while os.path.exists(nome_file):
        nome_file = f"{nome_base}_{cont}.txt"
        cont += 1
    
    return nome_file

def main():
    # Input dall'utente
    root_dir = input("Inserisci la directory da esplorare: ")
    stringa = input("Inserisci la stringa da cercare: ")

    # Modalità di output
    print("\nScegli la modalità di output:")
    print("1. Console")
    print("2. File")
    print("3. Entrambe")
    scelta = input("Scegli (1-3): ")

    modo = {"1": "console", "2": "file",  "3": "entrambe"}[scelta] if scelta in ["1","2","3"] else "console"
    
    file_output = None
    if modo in ["file", "entrambe"]:
        file_output = input("Inserisci il nome del file di output (default: risultati_ricerca.txt): ").strip() or "risultati_ricerca.txt"
        file_output = preparazione_file_output(file_output)

    # Esegui la ricerca
    risultati_testo, risultati_immagine, risultati_nome = ricerca_file(root_dir, stringa)

    # Stampa risultati
    stampa_risultati(risultati_testo, risultati_immagine, risultati_nome, stringa, modo, file_output)
    
    

if __name__ == "__main__":
    main()