import requests
import base64
import re

from myjson import *

google_api_key: str
with open("../gemini-api-key.txt","r") as f:
    google_api_key = f.line.strip()
base_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def generate_content(prompt, image_path=None):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": google_api_key,
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    if image_path:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        image_part = {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_data).decode('utf-8')
            }
        }
        data["contents"][0]["parts"].append(image_part)
    
    response = requests.post(base_api_url, headers=headers, json=data)
    return response.json()


def convert_markdown_to_html(text):
    # Grassetti
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Corsivo
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Titoli
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    
    # Liste (come prima)
    lines = text.split('\n')
    in_list = False
    converted_lines = []
    
    for line in lines:
        if line.strip().startswith('* '):
            if not in_list:
                converted_lines.append('<ul>')
                in_list = True
            converted_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                converted_lines.append('</ul>')
                in_list = False
            converted_lines.append(line)
    
    if in_list:
        converted_lines.append('</ul>')
    
    return '\n'.join(converted_lines)