import requests
import base64

def search(tipo, file_path) -> str:
    """
    tipo: 1 per PDF, 2 per DOCX, 3 per immagini
    """
    data = None # Contenuto da mandare a Gemini
    mime_type = "" # Tipo di contenuto da mandare a Gemini
    prompt = "" # Promt da mandare a Gemini
    google_api_key: str
    with open("../../gemini-api-key.txt","r") as f:
        google_api_key = f.line.strip()

    try:
        if tipo == 1:  # PDF
            mime_type = "application/pdf"
            with open(file_path, "rb") as file:
                data = file.read()
            prompt = "Leggi il contenuto di questo documento PDF e facci un riassunto in testo normale"
        
        elif tipo == 2:  # DOCX
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            with open(file_path, "rb") as file:
                data = file.read()
            prompt = "Leggi il contenuto di questo documento DOCX e facci un riassunto in testo normale"
        
        elif tipo == 3:  # Immagine
            mime_type = "image/jpeg"
            with open(file_path, "rb") as file:
                data = file.read()
            prompt = "Analizza l'immagine e descrivi in dettaglio il soggetto"

        headers = {
            "Content-tipo": "application/json",
            "x-goog-api-key": google_api_key
        }

        request_data = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64.b64encode(data).decode('utf-8')
                        }
                    }
                ]
            }]
        }

        base_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        response = requests.post(base_api_url, headers=headers, json=request_data)

        if response.status_code == 200:
            try:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception:
                print(f"Errore nella generazione del testo: {response.status_code}")
                return ""
        else:
            print(f"Errore API: {response.status_code}")
            return ""

    except Exception as e:
        print(f"Errore nel processare il file: {str(e)}")
        return ""
