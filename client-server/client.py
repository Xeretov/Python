import requests,json
from requests.auth import HTTPBasicAuth

base_api_url = "https://127.0.0.1:8080/"
username = ""
password = ""


def StampaMenuOperazioni():
    print("1. Inserisci cittadino")
    print("2. Leggi dati cittadino")
    print("3. Modifica cittadino")
    print("4. Elimina cittadino")
    print("5. Inserisci credenziali")
    print("6. Exit")
    comando = input("Inserisci operazione: ")
    return comando
    
def print_dictionary(dData):
    for keys, values in dData.items():
        print(keys + " - " + values)
        
def GetDatiCittadino():
    nome = input("Inserisci nome: ")
    cognome = input("Inserisci cognome: ")
    dataN = input("Inserisci data nascita(dd/mm/yyyy): ")
    codF = input("Inserisci codice fiscale: ")
    datiCittadino = {"nome":nome, "cognome": cognome, "dataNascita":dataN, "codFiscale":codF}
    return datiCittadino

def AcquisisciCredenziali():
    global username,password
    username = input("Inserisci username: ")
    password = input("Inserisci password: ")



print("Cosa vuoi fare?")
comando = StampaMenuOperazioni()
print("Comando inserito: " + comando)
if comando=="1":
    api_url = base_api_url + "add_cittadino"
    jsonDataRequest = GetDatiCittadino()
    response = requests.post(api_url,json=jsonDataRequest,verify=False,auth=HTTPBasicAuth(username,password))
    #print(response.json())
    print(response.status_code)
    print(response.headers["Content-Type"])
    data1 = response.json()
    if (type(response.json()) is dict):
            print_dictionary(response.json())
if comando == "5":
     AcquisisciCredenziali()