from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import os
import time

# Language codes: en=English, hi=Hindi, pa=Punjabi
def translate_text(text, target_language="hi", max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            translated = GoogleTranslator(source="auto", target=target_language).translate(text)
            
            if translated and ("Error 500" in translated or "Server Error" in translated):
                raise Exception("Google Translate ne error page bheja")
            
            return translated
        
        except Exception as e:
            print(f"Attempt {attempt} fail hua ({target_language}): {e}")
            if attempt < max_retries:
                time.sleep(attempt * 1.5)  # progressively lamba wait: 1.5s, 3s, 4.5s, 6s...
            else:
                return text  # translate na ho paye to original text hi dikhao, error message nahi

import os, tempfile, uuid

def text_to_speech(text, language="hi", output_file=None):
    try:
        tts = gTTS(text=text, lang=language)
        output_file = output_file or os.path.join(tempfile.gettempdir(), f"tts_{uuid.uuid4().hex}.mp3"); tts.save(output_file)
        return output_file
    except Exception:
        return None

def speech_to_text():
    """Mic se sunta hai. Mic disconnect/missing ho to bhi crash nahi hota."""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Bolo... (listening)")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Samajh nahi aaya, dobara bolo."
        except sr.RequestError:
            return "Internet connection check karo."

    except OSError:
        return "Mic connect nahi hai. Headset/mic check karke wapas try karo."
    except Exception as e:
        return f"Mic mein kuch problem hui: {str(e)[:100]}"

def process_text(text, target_language="hi"):
    """
    Ek text lo, translate karo, aur audio bhi bana do.
    Streamlit UI ya app.py se easily call karne ke liye.
    Returns: (translated_text, audio_file_path)
    """
    translated = translate_text(text, target_language)
    audio_file = text_to_speech(translated, target_language)
    return translated, audio_file

# Testing ke liye
if __name__ == "__main__":
    original_text = "What is the difference between supervised and unsupervised learning?"
    
    print("Original (English):")
    print(original_text)
    
    hindi_text = translate_text(original_text, "hi")
    print("\nTranslated (Hindi):")
    print(hindi_text)
    
    punjabi_text = translate_text(original_text, "pa")
    print("\nTranslated (Punjabi):")
    print(punjabi_text)
    
    audio_file = text_to_speech(hindi_text, "hi")
    print(f"\nAudio saved as: {audio_file}")
    print("\n--- Testing Speech-to-Text ---")
    spoken_text = speech_to_text()
    print("Tumne bola:")
    print(spoken_text)