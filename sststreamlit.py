import streamlit as st
import speech_recognition as sr
import pyttsx3
import os
import tempfile

# Function to speak the recognized command
def SpeakNow(command):
    voice = pyttsx3.init()
    voice.say(command)
    voice.runAndWait()

# Function to recognize speech based on selected language
def recognize_speech(audio_file, language):
    recognizer = sr.Recognizer()

    try:
        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)  # Read the entire audio file

        # Recognize speech in the selected language
        text = recognizer.recognize_google(audio, language=languages[language])
        st.success(f"Recognized ({language}): {text}")  # Show recognized text
        SpeakNow(text)  # Speak the recognized text
        st.write("Recognition complete.")
    except sr.UnknownValueError:
        st.error("Could not understand audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")

# Streamlit UI
st.title("Speech Recognition with Language Selection")
st.write("Choose a language and click 'Start Recording' to begin.")

# Language selection dropdown
languages = {
    "English": "en-US",
    "Kannada": "kn-IN",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Gujarati": "gu-IN",
    "Marathi": "mr-IN",
    "Bengali": "bn-IN",
    "Urdu": "ur-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE"
}

language = st.selectbox("Select Language:", list(languages.keys()))

# Button to start recording
if st.button("Start Recording"):
    st.write("Recording... Please speak into the microphone.")
    
    # Use a temporary file to store the recorded audio
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
        # Capture audio from the microphone
        os.system(f"python -m sounddevice -d 2 -r 44100 -c 1 -o {temp_audio_file.name}")

        # After recording is done
        st.write("Recording stopped. Processing...")

        # Recognize speech from the recorded audio
        recognize_speech(temp_audio_file.name, language)
