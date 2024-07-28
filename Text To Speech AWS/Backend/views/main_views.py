import os
from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import io

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/text-to-speech', methods=['GET', 'POST'])
def text_to_speech():
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
        
        # Navigate one directory back to save the audio file
        static_dir = os.path.join(os.path.dirname(os.getcwd()), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        tts.save(os.path.join(static_dir, audio_file))
        
    return render_template('text_to_speech.html', processed_text=processed_text, audio_file=audio_file)

@main.route('/speech-to-text', methods=['GET', 'POST'])
def speech_to_text():
    transcribed_text = None
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            return redirect(request.url)
        
        audio_file = request.files['audio_file']
        if audio_file.filename == '':
            return redirect(request.url)
        
        # Convert the audio file to PCM WAV using pydub
        try:
            audio = AudioSegment.from_file(audio_file)
            audio_wav = io.BytesIO()
            audio.export(audio_wav, format='wav')
            audio_wav.seek(0)

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_wav) as source:
                audio_data = recognizer.record(source)
            
            try:
                transcribed_text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                transcribed_text = "Google Web Speech could not understand audio"
            except sr.RequestError as e:
                transcribed_text = f"Could not request results from Google Web Speech service; {e}"
        
        except Exception as e:
            transcribed_text = f"Error processing audio file: {e}"
        
    return render_template('speech_to_text.html', transcribed_text=transcribed_text)

@main.route('/static/<path:filename>')
def download_file(filename):
    static_dir = os.path.join(os.path.dirname(os.getcwd()), 'static')
    return send_from_directory(static_dir, filename)
