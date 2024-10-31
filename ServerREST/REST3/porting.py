import os, sys
import dbclient as db
import json

mydb = db.connect()
if not mydb:
    print("Error connecting to database")
    sys.exit(1)
else:
    print("Connected to database")

cittadini: dict = {}
with open("anagrafe.json", "r") as json_file:
    cittadini = json.load(json_file)

for key, item in cittadini.items():
    cod_fiscale = key
    nome = item['nome']
    cognome = item['cognome']
    data_nascita = item['dataNascita']
    sQuery = "insert into cittadini(codice_fiscale,nome,cognome,data_nascita) "
    sQuery += f"values ('{cod_fiscale}','{nome}','{cognome}','{data_nascita}')"
    print(sQuery)
    db.write_in_db(mydb, sQuery)

db.close(mydb)