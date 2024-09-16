from flask import Flask, render_template, request
api = Flask("__name__")
utenti = [["mariorossi@gamil.com","mariorossi85","baubau66",0]]

@api.route('/registrati', methods=['GET'])
def registrati():
    utente=[]
    utente.append(request.args.get('email'))
    utente.append(request.args.get('cf'))
    utente.append(request.args.get('passw'))
    utente.append(0)
    if utente in utenti:
        return render_template('reg_ok.html')
    else:
        return render_template('reg_ko.html')

api.run(host="0.0.0.0", port=8085)