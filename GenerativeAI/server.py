from flask import Flask, render_template, request
import os
from generativeAI_tools import generate_content, convert_markdown_to_html

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    task = request.form['task']
    prompt = request.form['prompt']
    
    image_path = None
    if task == 'rispondereDomandaImg':
        image = request.files.get('image')
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], "image.png")
            image.save(image_path)
    
    if task == 'creareFavola':
        prompt = f"Crea una favola: {prompt}"
    elif task == 'rispondereDomanda':
        prompt = f"{prompt}"
    
    result = generate_content(prompt, image_path)
    
    # Extract the text from the result
    try:
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        print(result)
        if 'safetyRatings' in result['candidates'][0]:
            safety = result['candidates'][0]['safetyRatings']
            sexually_explicit = safety[0]['probability']
            hate_speech = safety[1]['probability']
            harassment = safety[2]['probability']
            dangerous_content = safety[3]['probability']
            dictionary = {'sexually_explicit':sexually_explicit,'hate_speech':hate_speech,'harassment':harassment,'dangerous_content':dangerous_content}
            print(f"Uno di questi filtri ha probabilità troppo alte di attivamento:\n{dictionary}")
            return f"Uno di questi filtri ha probabilità troppo alte di attivamento:\n{dictionary}"
        else:
            return "L'immagine caricata va contro le linee guida di Gemini."
    # Convert the markdown texto to html compatible
    html = convert_markdown_to_html(generated_text)
    return html

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)