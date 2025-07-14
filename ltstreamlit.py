import streamlit as st
from googletrans import Translator, LANGUAGES

def run_language_translator():
    st.title("Language Translator")

    # Initialize session state for input and output
    if 'input_value' not in st.session_state:
        st.session_state.input_value = ""
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = ""

    # Text input for translation
    input_value = st.text_area("Enter text", height=150, value=st.session_state.input_value)
    language_options = list(LANGUAGES.values())
    dest_lang = st.selectbox("Select Language", options=["choose language"] + language_options)

    if st.button("Detect and Translate"):
        if input_value.strip():
            translator = Translator()
            try:
                detected_language = translator.detect(input_value).lang
                detected_language_name = LANGUAGES[detected_language]
                st.write(f"Detected Language: **{detected_language_name}**")
                dest_language_code = [code for code, lang in LANGUAGES.items() if lang.lower() == dest_lang.lower()]
                
                if not dest_language_code or dest_lang == "choose language":
                    st.error("Error: Invalid destination language.")
                else:
                    dest_language_code = dest_language_code[0]
                    if detected_language == dest_language_code:
                        st.error("Error: Same language translation is not allowed.")
                    else:
                        translated = translator.translate(text=input_value, dest=dest_language_code)
                        st.session_state.translated_text = translated.text
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter text to translate.")

    # Display translated text if available
    if st.session_state.translated_text:
        st.write("Translated Language:")
        st.text_area("", st.session_state.translated_text, height=150)

    if st.button("Clear"):
        st.session_state.input_value = ""
        st.session_state.translated_text = ""
        # Optionally reset the selectbox
        dest_lang = "choose language"

# Run the Streamlit app
if __name__ == "__main__":
    run_language_translator()
