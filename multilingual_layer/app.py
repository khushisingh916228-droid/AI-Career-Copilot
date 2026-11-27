import streamlit as st
from main import translate_text, text_to_speech, speech_to_text

st.set_page_config(page_title="Multilingual Layer", page_icon="🌐")

st.title("🌐 Multilingual Layer")
st.write("Type or speak your text, then translate it into Hindi/Punjabi and listen to it.")

# Language selection
language_options = {"English": "en", "Hindi": "hi", "Punjabi": "pa"}
selected_language = st.selectbox("Target language chuno:", list(language_options.keys()))
lang_code = language_options[selected_language]

# Choose the input method: type or speak
input_method = st.radio("How would you like to give input?", ["Type", "Speak with mic"])

user_text = ""

if input_method == "Type":
    user_text = st.text_area("Enter your text here:", "")
    
    if st.button("Translate"):
        if user_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Translating..."):
                translated = translate_text(user_text, lang_code)
            
            st.subheader(f"Translated ({selected_language}):")
            st.write(translated)
            
            with st.spinner("Generating audio..."):
                audio_file = text_to_speech(translated, lang_code)
            
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

else:  # Speak with mic
    if st.button("Start speaking"):
        with st.spinner("Listening... please speak"):
            spoken = speech_to_text()
        
        st.subheader("Tumne bola:")
        st.write(spoken)
        
        if spoken and "Could not understand" not in spoken and "your internet connection" not in spoken:
            with st.spinner("Translating..."):
                translated = translate_text(spoken, lang_code)
            
            st.subheader(f"Translated ({selected_language}):")
            st.write(translated)
            
            with st.spinner("Generating audio..."):
                audio_file = text_to_speech(translated, lang_code)
            
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")