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
            print(f"Attempt {attempt} failed ({target_language}): {e}")
            if attempt < max_retries:
                time.sleep(attempt * 1.5)  # progressively lamba wait: 1.5s, 3s, 4.5s, 6s...
            else:
                return text  # if translation fails, show the original text, not an error message

import os, tempfile, uuid

def text_to_speech(text, language="hi", output_file=None):
    try:
        tts = gTTS(text=text, lang=language)
        output_file = output_file or os.path.join(tempfile.gettempdir(), f"tts_{uuid.uuid4().hex}.mp3"); tts.save(output_file)
        return output_file
    except Exception:
        return None

def speech_to_text(language="en-IN"):
    """Listens from the mic. Does not crash if the mic is disconnected or missing."""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... speak now")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Could not understand, please speak again."
        except sr.RequestError:
            return "Please check your internet connection."

    except OSError:
        return "Microphone not connected. Please check your headset/mic and try again."
    except Exception as e:
        return f"There was a problem with the microphone: {str(e)[:100]}"

def process_text(text, target_language="hi"):
    """
    Takes a text, translates it, and also generates audio.
    Made to be called easily from the Streamlit UI or app.py.
    Returns: (translated_text, audio_file_path)
    """
    translated = translate_text(text, target_language)
    audio_file = text_to_speech(translated, target_language)
    return translated, audio_file

# For testing
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