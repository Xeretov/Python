import requests, base64

def getImgText(path):
    # Image to Text Conversion
    image_data: bytes
    with open(path, "rb") as image_file:
        image_data = image_file.read()
        

    # Gemini API Prompt and URL
    prompt = f"Analizza l'immagine e descrivi in un unica parola italiana il soggetto"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": "AIzaSyCCm6Aoj2M18Gho95y7LEYIcCG9NjAIYdE"
    }

    data = {"contents":
            [
                {"parts":
                    [   
                        {"text": prompt},
                        {"inline_data":
                            {"mime_type": "image/jpeg", "data": base64.b64encode(image_data).decode('utf-8')}
                        }
                    ]
                }
            ]
        }   
    base_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    # Send the prompt to the Gemini API (replace with your API key)
    response = requests.post(base_api_url, headers=headers, json=data)
    # Parse the response
    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return ""