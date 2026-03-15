import streamlit as st
import google.generativeai as genai

# Streamlit'in güvenli kasasından (Secrets) API anahtarımızı alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Hızlı ve etkili Gemini modelini seçiyoruz
model = genai.GenerativeModel('gemini-2.5-flash')

# Sistem Komutu (Yapay zekanın karakteri)
system_prompt = """
Sen Kuran ve Sünnet ışığında şefkatle teselli veren manevi bir rehbersin.
Kullanıcıyı anla, yargılama ve derdine uygun 1 ayet ve 1 hadis ile kısa, anlaşılır bir teselli ver. Asla fetva verme.
"""

st.set_page_config(page_title="Manevi Rehber", page_icon="🌿")
st.title("🌿 Manevi Rehber")
st.write("Derdini yaz, Kuran ve Sünnet ışığında teselli bul...")

kullanici_derdi = st.text_area("İçinden geçenleri buraya yazabilirsin:")

if st.button("Tavsiye Al"):
    if kullanici_derdi:
        with st.spinner("Senin için ayet ve hadislere bakılıyor... Lütfen bekle."):
            tam_mesaj = f"{system_prompt}\n\nKullanıcının Derdi: {kullanici_derdi}"
            cevap = model.generate_content(tam_mesaj)
            
            st.success("İşte senin için bir teselli:")
            st.write(cevap.text)
    else:
        st.warning("Lütfen önce yukarıdaki kutuya bir şeyler yazın.")
