import streamlit as st
from main import translate_text, text_to_speech, speech_to_text

st.set_page_config(page_title="Multilingual Layer", page_icon="🌐")

st.title("🌐 Multilingual Layer")
st.write("Apna text likho ya bolo, aur Hindi/Punjabi mein translate + suno.")

# Language select karne ka option
language_options = {"English": "en", "Hindi": "hi", "Punjabi": "pa"}
selected_language = st.selectbox("Target language chuno:", list(language_options.keys()))
lang_code = language_options[selected_language]

# Tab se choose karo: type karo ya bolo
input_method = st.radio("Input kaise doge?", ["Type karo", "Mic se bolo"])

user_text = ""

if input_method == "Type karo":
    user_text = st.text_area("Apna text yahan likho:", "")
    
    if st.button("Translate karo"):
        if user_text.strip() == "":
            st.warning("Pehle kuch text likho.")
        else:
            with st.spinner("Translate ho raha hai..."):
                translated = translate_text(user_text, lang_code)
            
            st.subheader(f"Translated ({selected_language}):")
            st.write(translated)
            
            with st.spinner("Audio ban raha hai..."):
                audio_file = text_to_speech(translated, lang_code)
            
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

else:  # Mic se bolo
    if st.button("Bolna shuru karo"):
        with st.spinner("Sun rahi hoon... bolo"):
            spoken = speech_to_text()
        
        st.subheader("Tumne bola:")
        st.write(spoken)
        
        if spoken and "Samajh nahi aaya" not in spoken and "Internet connection" not in spoken:
            with st.spinner("Translate ho raha hai..."):
                translated = translate_text(spoken, lang_code)
            
            st.subheader(f"Translated ({selected_language}):")
            st.write(translated)
            
            with st.spinner("Audio ban raha hai..."):
                audio_file = text_to_speech(translated, lang_code)
            
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")