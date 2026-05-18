import streamlit as st
from gtts import gTTS
import io
import streamlit.components.v1 as components

# Sayfa Yapılandırması ve Sekme Bilgileri
st.set_page_config(
    page_title="İngilizce Telaffuz Alıştırması",
    page_icon="🗣️",
    layout="centered"
)

# Pastel, Renkli ve Çocuk Dostu CSS Tasarımları
st.markdown("""
    <style>
    /* Genel Arka Plan - Yumuşak ve Renkli Geçiş */
    .stApp {
        background: linear-gradient(135deg, #fef6fb 0%, #e6f0fa 100%);
    }
    
    /* Başlık */
    .main-title {
        color: #2b6cb0;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-size: 32px;
        margin-bottom: 5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Bilgilendirme Kutusu */
    .info-box {
        background-color: #ffffff;
        border: 2px dashed #bbeeeb;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 20px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #4a5568;
    }
    
    /* Yıldız Skor Göstergesi */
    .star-counter {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 2px solid #fde68a;
        border-radius: 24px;
        padding: 12px 24px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #d97706;
        box-shadow: 0 4px 6px rgba(217, 119, 6, 0.1);
        display: block;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("<h1 class='main-title'>🗣️ İngilizce Telaffuz Alıştırması</h1>", unsafe_allow_html=True)

# Kelimeler ve Türkçe Yaklaşık Okunuş İpuçları
word_hints = {
    "the": "dı / dıı",
    "join": "coyn",
    "jump": "camp",
    "who": "huu",
    "are": "aa",
    "think": "fink (dişlerin arasından s sızdırarak)",
    "thought": "foot (dişlerin arasından f/t sızdırarak)",
    "about": "ıbaut",
    "refuse": "rifyuz",
    "use": "yuz",
    "she": "şii",
    "chat": "çet",
    "accept": "eksept",
    "language": "lenguiç",
    "umbrella": "ambrella",
    "quick": "kuik",
    "what": "vat",
    "where": "vee",
    "three": "trii (dişlerin arasından t sızdırarak)",
    "speak": "spiik",
    "sign": "sayn",
    "location": "lokeyşın",
    "bathroom": "baatruum",
    "today": "tudey",
    "wednesday": "venzdey",
    "thursday": "förzdey",
    "watch": "voç",
    "rarely": "reerli",
    "usually": "yujıli",
    "generally": "cenırli",
    "currently": "karantli",
    "university": "yunivörsiti",
    "choose": "çuuz",
    "country": "kantri"
}

# Kelimeleri alfabetik sıraya göre dizelim
words = sorted(list(word_hints.keys()))

# Session State Hafızası
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "completed_words" not in st.session_state:
    st.session_state.completed_words = set()

# Üst Bilgilendirme ve Skor Tablosu
col_info, col_star = st.columns([2, 1])

with col_info:
    st.markdown("""
    <div class='info-box'>
        🎯 <b>Öğrenci Rehberi:</b><br>
        1️⃣ Listeden bir İngilizce kelime seç.<br>
        2️⃣ Doğru telaffuzu dinle (telaffuzu dinle butonu ile) ve kendi sesini kaydet.<br>
        3️⃣ Başarılı olduysan kutucuğu işaretle ve yıldızını kap!<br>
        💡 <b>Tureng Sözlük:</b> Kelime kutusuna <b>3 saniye basılı tutarak</b> doğrudan anlamına bakabilirsin.
    </div>
    """, unsafe_allow_html=True)

with col_star:
    st.markdown(f"<div class='star-counter'>⭐ Yıldızlarım: {st.session_state.stars}</div>", unsafe_allow_html=True)

# Kelime Seçim Listesi
selected_word = st.selectbox("🎯 Çalışmak istediğin İngilizce kelimeyi seç:", words)

# Tureng Entegrasyonlu İnteraktif Kelime Kutusu
word_box_html = f"""
<div id="word-container" style="
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    border: 3px solid #7dd3fc;
    border-radius: 20px;
    padding: 25px 15px;
    text-align: center;
    cursor: pointer;
    user-select: none;
    transition: all 0.2s ease;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
">
    <div style="font-size: 38px; font-weight: bold; color: #0369a1; letter-spacing: 0.5px;">{selected_word}</div>
    <div style="font-size: 15px; color: #0c4a6e; font-style: italic; margin-top: 8px;">📢 Okunuşu: {word_hints[selected_word]}</div>
    <div id="status" style="font-size: 11px; color: #0284c7; margin-top: 12px; font-weight: 500;">Sözlük için kelimeye 3 saniye basılı tutun...</div>
</div>

<script>
const container = document.getElementById('word-container');
const statusText = document.getElementById('status');
let pressTimer;

function startPress() {{
    container.style.transform = "scale(0.97)";
    container.style.background = "linear-gradient(135deg, #bae6fd 0%, #7dd3fc 100%)";
    statusText.innerText = "Bekleyin... Tureng Açılıyor...";
    pressTimer = window.setTimeout(function() {{
        window.open('https://tureng.com/tr/turkce-ingilizce/{selected_word}', '_blank');
        statusText.innerText = "Sözlük açıldı!";
        resetStyle();
    }}, 3000);
}}

function cancelPress() {{
    clearTimeout(pressTimer);
    resetStyle();
}}

function resetStyle() {{
    container.style.transform = "scale(1)";
    container.style.background = "linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)";
    statusText.innerText = "Sözlük için kelimeye 3 saniye basılı tutun...";
}}

container.addEventListener('mousedown', startPress);
container.addEventListener('mouseup', cancelPress);
container.addEventListener('mouseleave', cancelPress);
container.addEventListener('touchstart', function(e) {{ startPress(); }});
container.addEventListener('touchend', cancelPress);
container.addEventListener('touchcancel', cancelPress);
</script>
"""

components.html(word_box_html, height=160)

st.markdown("---")

# 1. ADIM: Doğru Telaffuzu Dinleme
st.write("### 📢 1. Telaffuzu Dinle")
try:
    tts = gTTS(text=selected_word, lang='en', tld='com')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format='audio/mp3')
except Exception as e:
    st.error("Ses yüklenirken bir hata oluştu.")

st.markdown("---")

# 2. ADIM: Öğrencinin Kendi Sesini Kaydetmesi
st.write("### 🎤 2. Kendi Sesini Kaydet ve Karşılaştır")
st.caption("Not: Ses veriniz android cihazlarda ve diğer tarayıcılarda gizli tutulur, sunucuya yüklenmez.")
audio_value = st.audio_input("Mikrofonu etkinleştirmek için aşağıdaki yuvarlağa basın ve konuşun:")

if audio_value:
    st.write("👇 Sizin ses kaydınız:")
    st.audio(audio_value, format="audio/wav")

st.markdown("---")

# 3. ADIM: Başarı İşaretleme ve Konfeti Patlatma
st.write("### ⭐ 3. Başarı Durumu")

is_already_done = selected_word in st.session_state.completed_words

is_checked = st.checkbox(
    "🎉 Bu kelimeyi doğru telaffuz etmeyi başardım!", 
    value=is_already_done, 
    key=f"check_{selected_
