import streamlit as st
from gtts import gTTS
import os
import pygame
import tempfile
import time
import uuid

def run_text_to_speech():
    st.title("Text-to-Speech")
    languages = ['English', 'Hindi', 'Kannada', 'Tamil', 'Telugu', 'Bengali', 'Gujarati', 'Marathi', 'Urdu', 'Punjabi', 
                 'Spanish', 'French', 'German', 'Chinese (Mandarin)', 'Japanese', 'Russian', 'Arabic']
    language_map = {
        'English': 'en', 'Hindi': 'hi', 'Kannada': 'kn', 'Tamil': 'ta', 'Telugu': 'te', 'Bengali': 'bn', 
        'Gujarati': 'gu', 'Marathi': 'mr', 'Urdu': 'ur', 'Punjabi': 'pa', 'Spanish': 'es', 'French': 'fr', 
        'German': 'de', 'Chinese (Mandarin)': 'zh-CN', 'Japanese': 'ja', 'Russian': 'ru', 'Arabic': 'ar'
    }

    text = st.text_area("Enter text here", height=200)
    selected_language = st.selectbox("Select Language", languages)

    if st.button("Play"):
        if text.strip() == "":
            st.warning("Please enter text to convert to speech!")
        else:
            language_code = language_map.get(selected_language, 'en')
            tts = gTTS(text=text, lang=language_code, slow=False)

            temp_path = tempfile.gettempdir()
            unique_filename = f"temp_{uuid.uuid4()}.mp3"
            filename = os.path.join(temp_path, unique_filename)
            tts.save(filename)

            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.unload()
            os.remove(filename)

            st.success(f"Played in {selected_language}")
