import streamlit as st
from gtts import gTTS
import io
from streamlit_mic_recorder import mic_recorder

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Let's Speak Right 🌟",
    page_icon="🎈",
    layout="centered"
)

# Çocuk dostu tasarım (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFF5E1; }
    h1 { color: #FF6B6B; font-family: 'Comic Sans MS', cursive, sans-serif; text-align: center; margin-bottom: 20px; }
    h3 { color: #4D96FF; font-family: 'Comic Sans MS', sans-serif; }
    .tip-box { background-color: #E1FFB1; padding: 15px; border-radius: 15px; border: 2px dashed #6BCB77; margin-bottom: 20px; color: #2C3E50; }
    .star-counter { font-size: 24px; font-weight: bold; text-align: center; background-color: #6BCB77; padding: 10px; border-radius: 20px; color: white; }
    .privacy-note { font-size: 12px; color: #7F8C8D; text-align: center; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# 2. Kelime Sözlüğü
WORDS_DATA = {
    "the": {"sound": "dı", "tip": "Dilini üst dişlerinin arkasına hafifçe değdirerek 'dı' de!"},
    "join": {"sound": "coyn", "tip": "Eğlenceli bir partiye 'coyn' diye katıldığını hayal et!"},
    "jump": {"sound": "camp", "tip": "'C' sesiyle başla ve yukarı zıpla: Camp!"},
    "who": {"sound": "huu", "tip": "Bir baykuş gibi 'huu' diye seslen!"},
    "are": {"sound": "aar", "tip": "Bir korsan gibi 'Aaar!' de!"},
    "think": {"sound": "fink", "tip": "Dilinin ucunu ısırarak 'fink' demeye çalış!"},
    "thought": {"sound": "foot", "tip": "Biraz zor bir kelime, dilini ısır ve 'foot' de!"},
    "about": {"sound": "ebaut", "tip": "'E-baut' şeklinde hızlıca söyle!"},
    "refuse": {"sound": "rifyuz", "tip": "Kabul etmiyorum derken 'rifyuz' de!"},
    "use": {"sound": "yuz", "tip": "Bilgisayar 'yüzü' gibi 'yuz' de!"},
    "she": {"sound": "şii", "tip": "Sessiz ol der gibi 'Şşşii' de!"},
    "chat": {"sound": "çet", "tip": "Arkadaşlarınla 'çet' yapıyormuş gibi!"},
    "accept": {"sound": "eksept", "tip": "Hediyeyi 'eksept' (kabul) et!"},
    "language": {"sound": "lengüic", "tip": "Konuştuğumuz diller birer 'lengüic'tir!"},
    "umbrella": {"sound": "ambırela", "tip": "Yağmurda 'ambırela'nı açmayı unutma!"},
    "quick": {"sound": "kuik", "tip": "Çok hızlı bir şekilde 'kuik' de!"},
    "what": {"sound": "vat", "tip": "Şaşkınlıkla 'Vat?' (Ne?) de!"},
    "where": {"sound": "veer", "tip": "Nerede arıyorsan 'Veer' orası!"},
    "three": {"sound": "fırii", "tip": "Dilini dişlerinin arasına al ve 'fırii' de (3)!"},
    "speak": {"sound": "spiyk", "tip": "İngilizce konuşurken 'spiyk' yapıyoruz!"},
    "sign": {"sound": "sayn", "tip": "İmza atar gibi 'sayn' de!"},
    "location": {"sound": "lokeşın", "tip": "Haritadaki yerimiz 'lokeşın'!"},
    "bathroom": {"sound": "baatruum", "tip": "Banyoya giderken 'baatruum' diyoruz!"},
    "today": {"sound": "tudey", "tip": "Bugün günlerden 'tudey'!"},
    "wednesday": {"sound": "venzdey", "tip": "Çarşamba günleri 'venzdey' diye okunur!"},
    "thursday": {"sound": "förzdey", "tip": "Perşembe günü dilini ısırıp 'förzdey' de!"},
    "watch": {"sound": "voç", "tip": "Kolundaki saate 'voç' diye bak!"},
    "rarely": {"sound": "reerli", "tip": "Çok nadir yapılan şeyler 'reerli'dir!"},
    "usually": {"sound": "yujuıli", "tip": "Genelde yaptığın şeylere 'yujuıli' de!"},
    "generally": {"sound": "cenırli", "tip": "Genel olarak 'cenırli' konuşuruz!"},
    "currently": {"sound": "karentli", "tip": "Şu anda, tam şimdi: 'karentli'!"},
    "university": {"sound": "yunivörsiti", "tip": "Büyüyünce gideceğin 'yunivörsiti'!"},
    "choose": {"sound": "çuuz", "tip": "En güzel oyuncağı 'çuuz' (seç)!"},
    "country": {"sound": "kantri", "tip": "Yaşadığımız güzel ülke bir 'kantri'dir!"}
}

if "stars" not in st.session_state:
    st.session_state.stars = 0

# YENİ BAŞLIK
st.markdown("<h1>🎈 Let's Speak Right 🎈</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"<div class='star-counter'>⭐ Yıldızlarım: {st.session_state.stars}</div>", unsafe_allow_html=True)
    st.write("---")
    st.write("### 🎮 Nasıl Oynanır?")
    st.write("1. Kelime seç. \n2. Dinle. \n3. Kendi sesini kaydet. \n4. Başardım butonuna bas!")

selected_word = st.selectbox("👉 Bir kelime seç:", options=list(WORDS_DATA.keys()))

if selected_word:
    st.markdown(f"### 🔤 Kelime: **{selected_word}**")
    st.markdown(f"🗣️ **Okunuşu:** *{WORDS_DATA[selected_word]['sound']}*")
    st.markdown(f"<div class='tip-box'>💡 <b>İpucu:</b> {WORDS_DATA[selected_word]['tip']}</div>", unsafe_allow_html=True)
    
    try:
        tts = gTTS(text=selected_word, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp.getvalue(), format='audio/mp3')
    except:
        st.error("Ses yüklenemedi, lütfen tekrar deneyin.")

    st.write("---")
    st.markdown("### 🎙️ Şimdi Sen Söyle!")
    
    audio_recorder = mic_recorder(
        start_prompt="🔴 Kaydı Başlat",
        stop_prompt="⏹️ Kaydı Bitir",
        key=f"r_{selected_word}"
    )
    
    if audio_recorder:
        st.audio(audio_recorder['bytes'], format='audio/wav')
        st.success("Harika gidiyorsun!")

    st.write("---")
    
    if st.button("🎉 BAŞARDIM! 🌟", use_container_width=True):
        st.session_state.stars += 1
        st.balloons()
        st.rerun()

st.markdown("<div class='privacy-note'>🔒 Sesin kaydedilmez, her şey senin tarayıcında kalır. 😊</div>", unsafe_allow_html=True)

Uygulamanızın yeni ismi "Let's Speak Right" hayırlı olsun! Herhangi bir başka değişiklik isterseniz buradayım.
