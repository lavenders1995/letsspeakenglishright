import streamlit as str
from gtts import gTTS
import io
from streamlit_mic_recorder import mic_recorder  # Yeni ve hatasız kütüphane

# Sayfa Genişliği ve Başlığı
str.set_page_config(page_title="İngilizce Telaffuz Alıştırması", page_icon="🇬🇧", layout="centered")

# --- Pastel ve Estetik CSS Dokunuşları ---
str.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc;
    }
    .main-title {
        color: #4a5568;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        padding: 10px;
    }
    .word-box {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .star-box {
        background-color: #fef3c7;
        border: 1px solid #fde68a;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #d97706;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_with_html=True)

# --- Başlık ---
str.markdown("<h1 class='main-title'>🗣️ İngilizce Telaffuz Alıştırması</h1>", unsafe_with_html=True)

# --- Kelime Listesi ---
words = [
    "the", "join", "jump", "who", "are", "think", "thought", "about", 
    "refuse", "use", "she", "chat", "accept", "language", "umbrella", 
    "quick", "what", "where", "three", "speak", "sign", "location", 
    "bathroom", "today", "wednesday", "thursday", "watch", "rarely", 
    "usually", "generally", "currently", "university", "choose", "country"
]

# --- Session State (Yenileyince Sıfırlanan Hafıza) ---
if "stars" not in str.session_state:
    str.session_state.stars = 0
if "completed_words" not in str.session_state:
    str.session_state.completed_words = set()

# --- Yıldız Skor Tablosu ---
str.markdown(f"""
    <div class='star-box'>
        ⭐ Toplam Başarı Yıldızı: {str.session_state.stars}
    </div>
""", unsafe_with_html=True)

# --- Kelime Seçim Alanı ---
str.markdown("<div class='word-box'>", unsafe_with_html=True)
selected_word = str.selectbox("Çalışmak istediğin kelimeyi listeden seç:", words)
str.markdown(f"### Seçilen Kelime: <span style='color:#3182ce;'>{selected_word}</span>", unsafe_with_html=True)
str.markdown("</div>", unsafe_with_html=True)

# --- Çalışma Alanı ---
str.markdown("<div class='word-box'>", unsafe_with_html=True)
str.write("##### 1. Doğru Telaffuzu Dinle")

# Telaffuzu dinle kısmı
tts = gTTS(text=selected_word, lang='en', tld='com')
fp = io.BytesIO()
tts.write_to_fp(fp)
fp.seek(0)

str.audio(fp, format='audio/mp3')
str.markdown("</div>", unsafe_with_html=True)

# --- Ses Kayıt ve Karşılaştırma Alanı ---
str.markdown("<div class='word-box'>", unsafe_with_html=True)
str.write("##### 2. Kendi Sesini Kaydet ve Karşılaştır")

# Kararlı ve temiz ses kayıt butonu
audio_record = mic_recorder(
    start_prompt="🔴 Kaydı Başlat",
    stop_prompt="⏹️ Kaydı Durdur",
    just_once=False,
    key='recorder'
)

if audio_record:
    # Kaydedilen sesi anında ekranda oynatır
    str.audio(audio_record['bytes'], format='audio/wav')
    str.info("Yukarıdaki oynatıcıdan kendi sesini dinle ve doğru telaffuzla karşılaştır!")

str.markdown("</div>", unsafe_with_html=True)

# --- Başarı ve Yıldız Mekanizması ---
str.markdown("<div class='word-box'>", unsafe_with_html=True)
str.write("##### 3. Başarı Durumu")

if selected_word not in str.session_state.completed_words:
    if str.button(f"✨ '{selected_word}' Kelimesini Doğru Okudum, Yıldızı Kap!"):
        str.session_state.stars += 1
        str.session_state.completed_words.add(selected_word)
        str.rerun()
else:
    str.success(f"🎉 Tebrikler! '{selected_word}' kelimesinden zaten bir yıldız kazandın.")

str.markdown("</div>", unsafe_with_html=True)

# --- Alt Bilgi ---
str.markdown("""
    <hr style='border-top: 1px dashed #cbd5e0;'>
    <p style='text-align: center; color: #a0aec0; font-size: 12px;'>
        Bu uygulama tamamen gizlilik dostudur. Mikrofon izinleri sadece anlık dinleme içindir, 
        ses verileriniz asla bir yere kaydedilmez. Sayfa yenilendiğinde tüm veriler silinir.<br>
        <i>Mobil cihazlarda ve özellikle android cihazlarda Chrome kullanılması önerilir.</i>
    </p>
""", unsafe_with_html=True)
