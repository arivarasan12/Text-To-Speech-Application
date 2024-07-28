import os
from flask import Blueprint, render_template, request, send_from_directory
from gtts import gTTS

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    processed_text = None
    audio_file = None
    if request.method == 'POST':
        input_text = request.form['input_text']
        voice = request.form['voice']
        tld = request.form['accent'] if request.form['accent'] else 'com'
        
        processed_text = f"Processed text: {input_text}"
        
        # Generate MP3 from input text with selected language and accent
        tts = gTTS(input_text, lang=voice, tld=tld)
        audio_file = "output.mp3"
        
        # Ensure the static directory exists
        static_dir = os.path.join(os.getcwd(), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        static_dir="C:\\Users\\ariva\\OneDrive\\Desktop\\Text To Speech AWS\\Backend\\static"
        tts.save(os.path.join(static_dir, audio_file))
        
    return render_template('index.html', processed_text=processed_text, audio_file=audio_file)

@main.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename)
