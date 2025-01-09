from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Percorso del database
pathDB = 'database/'

# Inizializzazione file JSON se non esistono
for file in ['case_in_affitto.json', 'case_in_vendita.json', 'filiali.json', 'affitti_casa.json', 'vendite_casa.json']:
    if not os.path.isfile(pathDB + file):
        with open(pathDB + file, "w") as json_file:
            json.dump({}, json_file)

# Cerca case in vendita
@app.route('/cerca_casa_vendita', methods=['POST'])
def cerca_casa_vendita():
    with open(pathDB + 'case_in_vendita.json', 'r') as file:
        case_in_vendita = json.load(file)
    return jsonify(case_in_vendita)

# Cerca case in affitto
@app.route('/cerca_casa_affitto', methods=['POST'])
def cerca_casa_affitto():
    with open(pathDB + 'case_in_affitto.json', 'r') as file:
        case_in_affitto = json.load(file)
    return jsonify(case_in_affitto)

# Viene registrata la vendita di una casa
@app.route('/venduta_casa', methods=['POST'])
def venduta_casa():
    data = request.json
    catastale = data['catastale']
    vendite_casa = {}
    case_in_vendita = {}
    # Prende dati dal database
    with open(pathDB + 'vendite_casa.json', 'r') as file:
        vendite_casa = json.load(file)
    with open(pathDB + 'case_in_vendita.json', 'r') as file:
        case_in_vendita = json.load(file)
    # Controlla se il catastale inserito esiste e non sia già venduto
    if catastale not in case_in_vendita:
        return jsonify({'errore': 'La casa non è presente nel database'})
    if catastale in vendite_casa:
        return jsonify({'errore': 'La casa è già stata venduto'})
    # Crea un nuovo record di vendita
    casa = case_in_vendita[catastale]
    to_add = {
        catastale:{
            "data_vendita": data['data_vendita'],
            "filiale_proponente": casa['filiale_proponente'],
            "filiale_venditrice": data['filiale_venditrice'],
            "prezzo": casa['prezzo']
        }
    }
    # Aggiorna il database
    vendite_casa.update(to_add)
    with open(pathDB + 'vendite_casa.json', 'w') as file:
        json.dump(vendite_casa, file, indent=4)
    return jsonify({"status": "success"})

# Viene registrata l'affittazione di una casa
@app.route('/affittata_casa', methods=['POST'])
def affittata_casa():
    data = request.json
    catastale = data['catastale']
    affitti_casa = {}
    case_in_affitto = {}
    # Prende dati dal database
    with open(pathDB + 'affitti_casa.json', 'r') as file:
        affitti_casa = json.load(file)
    with open(pathDB + 'case_in_affitto.json', 'r') as file:
        case_in_affitto = json.load(file)
    # Controlla se il catastale inserito esiste e non sia già affittato
    if catastale not in case_in_affitto:
        return jsonify({"status": "error", "message": "La casa non è presente nel database"})
    if catastale in affitti_casa:
        return jsonify({"status": "error", "message": "La casa è già affittata"})
    # Crea un nuovo record di affitto
    casa = case_in_affitto[catastale]
    to_add = {
        catastale: {
            "data_affitto": data['data_affitto'],
            "filiale_proponente": casa['filiale_proponente'],
            "filiale_venditrice": data['filiale_venditrice'],
            "prezzo_affitto": casa['prezzo_mensile'],
            "durata_contratto": str(data['durata_contratto'])+" mesi"
        }
    }
    # Aggiorna il database
    affitti_casa.update(to_add)
    with open(pathDB + 'affitti_casa.json', 'w') as file:
        json.dump(affitti_casa, file, indent=4)
    return jsonify({"status": "success"}), 200

# Crea un report di vendite e affitti di tutte le filiali per ogni mese
@app.route('/report_vendite_affitti', methods=['POST'])
def report_vendite_affitti():
    data = request.json
    data_inizio = data['data_inizio']
    data_fine = data['data_fine']
    vendite_casa = {}
    affitti_casa = {}
    # Prende dati dal database
    with open(pathDB + 'vendite_casa.json', 'r') as file:
        vendite_casa = json.load(file)
    with open(pathDB + 'affitti_casa.json', 'r') as file:
        affitti_casa = json.load(file)
    
    report = {}
    # Per ogni mese aumenta di uno il valore di vendita e affitto di una filiale
    for key, value in vendite_casa.items():
        if data_inizio <= value['data_vendita'] <= data_fine:
            mese = value['data_vendita'][:7]
            filiale = value['filiale_venditrice']
            if filiale not in report:
                report[filiale] = {}
            if mese not in report[filiale]:
                report[filiale][mese] = {'vendite': 0, 'affitti': 0}
            report[filiale][mese]['vendite'] += 1
    
    for key, value in affitti_casa.items():
        if data_inizio <= value['data_affitto'] <= data_fine:
            mese = value['data_affitto'][:7]
            filiale = value['filiale_venditrice']
            if filiale not in report:
                report[filiale] = {}
            if mese not in report[filiale]:
                report[filiale][mese] = {'vendite': 0, 'affitti': 0}
            report[filiale][mese]['affitti'] += 1

    return jsonify(report)

# Crea un report di vendite e affitti di una filiale
@app.route('/guadagno_filiali', methods=['POST'])
def guadagno_filiali():
    data = request.json
    filiale = data['filiale'].lower()
    data_inizio = data['data_inizio']
    data_fine = data['data_fine']
    vendite_casa = {}
    affitti_casa = {}
    guadagno = 0
    guadagno_mensile = 0
    # Prende dati dal database
    with open(pathDB + 'vendite_casa.json', 'r') as file:
        vendite_casa = json.load(file)
    with open(pathDB + 'affitti_casa.json', 'r') as file:
        affitti_casa = json.load(file)
    # Per ogni filiale che ha venduto o affittato aumenta il guadagno
    # (e.g. guadagno 3% per filiale che propone e vende altrimenti 1)
    for key, value in vendite_casa.items():
        if value['filiale_venditrice'].lower() == filiale and data_inizio <= value['data_vendita'] <= data_fine:
            prezzo_vendita = int(value['prezzo_vendita'])
            guadagno += (prezzo_vendita*3)/100 if filiale == value['filiale_proponente'] else (prezzo_vendita)/100
    for key, value in affitti_casa.items():
        if value['filiale_venditrice'].lower() == filiale and data_inizio <= value['data_affitto'] <= data_fine:
            guadagno_mensile += int(value['prezzo_affitto'])
    return jsonify({'guadagno': f"{guadagno:.2f}", 'guadagno_mensile': f"{guadagno_mensile:.2f}", 'guadagno_totale': f"{guadagno + guadagno_mensile:.2f}"})


if __name__ == '__main__':
    app.run(debug=True, port=8080)