import pytesseract
import docx
import pdfplumber
from googletrans import Translator
import os
import unicodedata
import streamlit as st

# Set the path to the Tesseract executable (if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Unified Unicode ranges for multiple languages
UNICODE_RANGES = {
    "Kannada": (0x0C80, 0x0CFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Hindi/Devanagari": (0x0900, 0x097F),
    "Malayalam": (0x0D00, 0x0D7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Bengali": (0x0980, 0x09FF),
    "Punjabi/Gurmukhi": (0x0A00, 0x0A7F),
    "Odia": (0x0B00, 0x0B7F),
    "Latin": (0x0041, 0x007A),
    "Cyrillic": (0x0400, 0x04FF),
    "Arabic": (0x0600, 0x06FF),
    "Chinese": (0x4E00, 0x9FFF),
    "Japanese": (0x3040, 0x309F),
    "Greek": (0x0370, 0x03FF),
    "Hebrew": (0x0590, 0x05FF),
    "Thai": (0x0E00, 0x0E7F),
}

# Function to detect the language based on Unicode range
def detect_unicode_language(text):
    for char in text:
        char_code = ord(char)
        for language, (start, end) in UNICODE_RANGES.items():
            if start <= char_code <= end:
                return language
    return "Unknown"

# Function to extract text from a PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

# Function to extract text from a plain text file
def extract_text_from_txt(file):
    return file.read().decode("utf-8")

# Function to split text into chunks of a specified size
def split_text_into_chunks(text, max_chars=500):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

# Function to translate text using googletrans
def translate_text(text, target_language='en'):
    translator = Translator()
    chunks = split_text_into_chunks(text, max_chars=500)
    translated_chunks = []

    for chunk in chunks:
        try:
            translation = translator.translate(chunk, dest=target_language)
            translated_chunks.append(translation.text)
        except Exception as e:
            print(f"Error translating chunk: {e}")
            continue

    return ' '.join(translated_chunks)

# Function to detect and translate text from different file types (PDF, DOCX, TXT)
def detect_and_translate(file, file_type, target_language='en'):
    if file_type == 'PDF':
        text = extract_text_from_pdf(file)
    elif file_type == 'DOCX':
        text = extract_text_from_docx(file)
    elif file_type == 'TXT':
        text = extract_text_from_txt(file)
    else:
        raise ValueError("Unsupported file type! Use 'PDF', 'DOCX', or 'TXT'.")
    
    # Detect Unicode language based on extracted text
    detected_language = detect_unicode_language(text)

    # Translate text
    translated_text = translate_text(text, target_language)
    
    return detected_language, translated_text

# Streamlit app
def run_file_reader():
    st.title("Language Detector & Translator")

    # Language dropdown
    languages = {
        "Kannada": "kn",
        "Telugu": "te",
        "Tamil": "ta",
        "Hindi": "hi",
        "Malayalam": "ml",
        "Gujarati": "gu",
        "Bengali": "bn",
        "Punjabi": "pa",
        "Odia": "or",
        "English": "en",
        "Cyrillic": "ru",
        "Arabic": "ar",
        "Chinese (Simplified)": "zh-cn",
        "Japanese": "ja",
        "Greek": "el",
        "Hebrew": "he",
        "Thai": "th",
    }

    language = st.selectbox("Select Language to Translate Into:", list(languages.keys()))
    target_language = languages[language]

    # File type dropdown
    file_type = st.selectbox("Select File Type:", ["PDF", "DOCX", "TXT"])

    # File upload
    file = st.file_uploader("Upload File", type=['pdf', 'docx', 'txt'])

    # Initialize session state for results
    if 'results' not in st.session_state:
        st.session_state.results = None

    # Clear previous results
    if st.button("Clear"):
        st.session_state.results = None

    # Perform translation if file is uploaded
    if file:
        detected_language, translated_text = detect_and_translate(file, file_type, target_language)
        st.session_state.results = (detected_language, translated_text)

    # Display results if available
    if st.session_state.results:
        detected_language, translated_text = st.session_state.results
        st.write(f"**Detected Language:** {detected_language}")
        st.write(f"**Translated Text:**\n{translated_text}")

# Run the Streamlit app
if __name__ == "__main__":
    run_file_reader()
