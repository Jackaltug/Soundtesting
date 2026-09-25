import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# Sık kullanılan dillerin eşleşme tablosu
LANGUAGES = {
    "1": ("de", "Almanca"),
    "2": ("tr", "Türkçe"),
    "3": ("en", "İngilizce"),
    "4": ("fr", "Fransızca"),
    "5": ("es", "İspanyolca"),
    "6": ("it", "İtalyanca"),
    "7": ("ru", "Rusça")
}

def get_target_language():
    print("\n--- Hedef Dil Seçimi ---")
    for key, (code, name) in LANGUAGES.items():
        print(f"{key}. {name} ({code})")
    print("8. Diğer (Dil kodunu manuel girin - örn: ja, ko, ar)")
    
    choice = input("\nÇevirmek istediğiniz dilin numarasını girin: ").strip()
    
    if choice in LANGUAGES:
        return LANGUAGES[choice]
    elif choice == "8":
        custom_code = input("Hedef dil kodunu girin (örn. 'ja' - Japonca): ").strip().lower()
        return (custom_code, custom_code)
    else:
        print("Geçersiz seçim yapıldı, varsayılan olarak Almanca ('de') seçildi.")
        return ("de", "Almanca")

# 1. Dil seçimini al
target_code, target_name = get_target_language()

# 2. Ses kaydı alma
duration = 5  # Kayıt süresi (saniye)
sample_rate = 44100

print("\n🎙️ Şimdi konuşun...")
recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)
sd.wait()
print("Kayıt tamamlandı.")

wav.write("output.wav", sample_rate, recording)

# 3. Ses dosyasını metne dönüştürme
recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

text = ""
try:
    # Konuşulan dili İngilizce ("en") olarak algılar, Türkçe için "tr-TR" yapabilirsiniz
    text = recognizer.recognize_google(audio, language="en")
    print("🗣️ Algılanan Metin:", text)
except sr.UnknownValueError:
    print("Konuşma tanınamadı.")
except sr.RequestError as e:
    print(f"Hizmet hatası: {e}")

# 4. Seçilen dile çeviri yapma
if text:
    translator = Translator()
    translated = translator.translate(text, dest=target_code)
    print(f"🌍 {target_name} Çevirisi:", translated.text)


