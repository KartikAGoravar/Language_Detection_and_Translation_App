import streamlit as st
from ltstreamlit import run_language_translator  # Importing function from ltstreamlit.py
from ttsstreamlit import run_text_to_speech  # Importing function from ttsstreamlit.py
from readingstreamlit import run_file_reader  # Importing function from readingstreamlit.py (if ready)
from sststreamlit import speech_to_text

# Frontend page for selecting an option
st.title("Select a Task")

# Dropdown to select between Language Translator, Text-to-Speech, and File Reader
task = st.selectbox("Choose your task", ["Select", "Language Translator", "Text-to-Speech", "File Reader"])

# Navigate to the respective app page based on the task selected
if task == "Language Translator":
    run_language_translator()  # Calls the function from ltstreamlit.py
elif task == "Text-to-Speech":
    run_text_to_speech()  # Calls the function from ttsstreamlit.py
elif task == "File Reader":
    run_file_reader()  # Calls the function from readingstreamlit.py
elif task == "Speech-to-text":
    run_speech_to_text() 