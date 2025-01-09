import requests
import json
import time

SERVER_URL = 'http://127.0.0.1:8080'

def cerca_casa_vendita():
    '''
    Cerca le case in vendita nel database e ritorna una lista di dizionari con le informazioni relative a ogni casa.
    '''
    print("\n--- CERCA CASE IN VENDITA ---")
    risultato = requests.post(f"{SERVER_URL}/cerca_casa_vendita")
    case_in_vendita = risultato.json()

    print("\nLista delle case in vendita:")
    for catastale, dettagli in case_in_vendita.items():
        print(f"\n- Catastale: {catastale}")
        print(f"- Indirizzo: {dettagli['indirizzo']} {dettagli['numero_civico']}")
        print(f"- Piano: {dettagli['piano']}")
        print(f"- Metri quadrati: {dettagli['metri']}")
        print(f"- Vani: {dettagli['vani']}")
        print(f"- Prezzo: €{dettagli['prezzo']}")
        print(f"- Stato: {'Libera' if dettagli['stato'] == 'LIBERO' else 'Occupata'}")
        print(f"- Filiale proponente: {dettagli['filiale_proponente']}")
    print("\n")

def cerca_casa_affitto():
    '''
    Cerca le case in affitto nel database e ritorna una lista di dizionari con le informazioni relative a ogni casa.
    '''
    print("\n--- CERCA CASE IN AFFITTO ---")
    risultato = requests.post(f"{SERVER_URL}/cerca_casa_affitto")
    case_in_affitto = risultato.json()

    print("\nLista delle case in affitto:")
    for catastale, dettagli in case_in_affitto.items():
        print(f"\n- Catastale: {catastale}")
        print(f"- Indirizzo: {dettagli['indirizzo']} {dettagli['civico']}")
        print(f"- Tipo affitto: {dettagli['tipo_affitto']}")
        print(f"- Bagno personale: {'Sì' if dettagli['bagno_personale'] else 'No'}")
        print(f"- Prezzo mensile: €{dettagli['prezzo_mensile']}")
        print(f"- Filiale proponente: {dettagli['filiale_proponente']}")
    print("\n")

def registra_vendita():
    '''
    Registra una casa che viene venduta nel database.
    '''
    print("\n--- REGISTRA VENDITA CASA ---")
    case_in_vendita = {}

    check = input("Vuoi vedere la lista delle case in vendita? (s): ")
    if check.lower() == 's':
        cerca_casa_vendita()


    catastale = input("Inserisci il catastale della casa: ").strip()
    
    data_vendita = time.strftime("%Y-%m-%d")
    filiale_venditrice = input("Inserisci la filiale venditrice: ").strip()
    
    data = {
        "catastale": catastale,
        "data_vendita": data_vendita,
        "filiale_venditrice": filiale_venditrice,
    }

    response = requests.post(f"{SERVER_URL}/venduta_casa", json=data)
    if response.status_code == 200:
        print("Casa venduta con successo!")
    else:
        print("Errore durante la vendita della casa:\n"+response["message"])

def registra_affitto():
    '''
    Registra una casa che viene affittata nel database.
    '''
    print("\n--- REGISTRA AFFITTO CASA ---")
    
    check = input("Vuoi vedere la lista delle case in affitto? (s): ")
    if check.lower() == 's':
        cerca_casa_affitto()

    catastale = input("Inserisci il catastale della casa: ").strip()
    
    
    data_affitto = time.strftime("%Y-%m-%d")
    filiale_venditrice = input("Inserisci la filiale venditrice: ").strip()
    durata_contratto = input("Inserisci la durata del contratto (es. 3, 6 o 12): ").strip()
    
    data = {
        "catastale": catastale,
        "data_affitto": data_affitto,
        "filiale_venditrice": filiale_venditrice,
        "durata_contratto": durata_contratto
    }
    
    response = requests.post(f"{SERVER_URL}/affittata_casa", json=data)
    if response.status_code == 200:
        print("Casa affittata con successo!")
    else:
        print("Errore durante l'affittazione della casa:\n"+response["message"])

def report_vendite_affitti():
    '''
    Genera un report sulle vendite e gli affitti delle case nel database.
    Crea un file JSON con i dati del report.
    '''
    print("\n--- GENERA REPORT VENDITE/AFFITTI ---")
    data_inizio = input("Inserisci la data di inizio (YYYY-MM-DD): ").strip()
    data_fine = input("Inserisci la data di fine (YYYY-MM-DD): ").strip()
    data = {
        "data_inizio": data_inizio,
        "data_fine": data_fine
    }
    risultato = requests.post(f"{SERVER_URL}/report_vendite_affitti", json=data)
    print(f"Report generato nel range {data_inizio} - {data_fine}:\n", risultato.json())
    name = str(time.strftime("%Y-%m-%d_%H%M%S"))
    with open("report_vendite_affitti_"+name+".json", "w") as file:
        json.dump(risultato.json(), file, indent=4)
    print("File report_vendite_affitti.json creato.")

def guadagno_filiali():
    '''
    Calcola il guadagno delle filiali per ogni casa nel database.
    '''
    print("\n--- CALCOLA GUADAGNO DELLE FILIALI ---")
    filiale = input("Inserisci il nome della filiale: ").strip()
    data_inizio = input("Inserisci la data di inizio (YYYY-MM-DD): ").strip()
    data_fine = input("Inserisci la data di fine (YYYY-MM-DD): ").strip()
    data = {
        "filiale": filiale,
        "data_inizio": data_inizio,
        "data_fine": data_fine
    }
    risultato = requests.post(f"{SERVER_URL}/guadagno_filiali", json=data)
    name = str(time.strftime("%Y-%m-%d_%H%M%S"))
    with open(f"guadagno_filiali_"+name+".json", "w") as file:
        json.dump(risultato.json(), file, indent=4)
    print(f"Guadagno della filiale {filiale.upper()}:\n", risultato.json())

def mostra_menu():
    '''
    Mostra il menu principale.
    '''
    global login
    print("\n--- MENU PRINCIPALE ---")
    print("1. Cerca case in vendita")
    print("2. Cerca case in affitto")
    print("3. Compra casa")
    print("4. Affitta casa")
    print("5. Login") if not login else ""
    print("6. Genera report vendite/affitti") if login else ""
    print("7. Calcola guadagno delle filiali") if login else ""
    print("8. Esci")

def logon():
    '''
    Effettua il login per accedere alle funzionalità riservate.
    '''
    username = input("Inserisci il tuo username: ").strip()
    password = input("Inserisci la tua password: ").strip()
    with open("utenti.json", "r") as file:
        utenti = json.load(file)
        if username in utenti and utenti[username] == password:
            return True
        else:
            return False
    

def main():
    '''
    Esecuzione del programma.
    '''
    global login
    login = False
    while True:
        mostra_menu()
        scelta = input("Seleziona un'opzione (1-8): ").strip()
        
        if scelta == '1':
            cerca_casa_vendita()
        elif scelta == '2':
            cerca_casa_affitto()
        elif scelta == '3':
            registra_vendita()
        elif scelta == '4':
            registra_affitto()
        elif scelta == '5' and login:
            print("Sei già loggato!")
        elif scelta == '5' and not login:
            login = logon()
        elif scelta in ['6','7'] and not login:
            print("Devi essere loggato per eseguire questa operazione")
        elif scelta == '6' and login:
            report_vendite_affitti()
        elif scelta == '7' and login:
            guadagno_filiali()
        elif scelta == '8':
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main()
