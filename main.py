import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# Sık kullanılan dillerin eşleşme tablosu
LANGUAGES = {
    "1": ("de", "German"),
    "2": ("tr", "Turkish"),
    "3": ("en", "English"),
    "4": ("fr", "French"),
    "5": ("es", "Spanish"),
    "6": ("it", "Italic"),
    "7": ("ru", "Russian")
}

def get_target_language():
    print("\n--- Main Language Choice ---")
    for key, (code, name) in LANGUAGES.items():
        print(f"{key}. {name} ({code})")
    print("8. Diğer (Enter language code manually - örn: ja, ko, ar)")
    
    choice = input("\nEnter the number of the language you want to translate into: ").strip()
    
    if choice in LANGUAGES:
        return LANGUAGES[choice]
    elif choice == "8":
        custom_code = input("Enter the target language code (örn. 'ja' - Japanese): ").strip().lower()
        return (custom_code, custom_code)
    else:
        print("Invalid selection made; defaulting to German ('de') seçildi.")
        return ("de", "German")


target_code, target_name = get_target_language()


duration = 5  
sample_rate = 44100

print("\n🎙️ Now Start Speaking...")
recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)
sd.wait()
print("Recording is finished.")

wav.write("output.wav", sample_rate, recording)


recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

text = ""
try:
    text = recognizer.recognize_google(audio, language="en")
    print("🗣️ Detected text:", text)
except sr.UnknownValueError:
    print("Speech not recognized.")
except sr.RequestError as e:
    print(f"Service error: {e}")


if text:
    translator = Translator()
    translated = translator.translate(text, dest=target_code)
    print(f"🌍 {target_name} Translation:", translated.text)


