import streamlit as st
import google.generativeai as genai

# Streamlit'in güvenli kasasından (Secrets) API anahtarımızı alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Hızlı ve etkili Gemini modelini seçiyoruz
model = genai.GenerativeModel('gemini-2.5-flash')

# 1. Geliştirilmiş Sistem Komutu (Karakter, Kurallar ve Nasihat Bölümü)
# Yapay zekaya dertli kullanıcıyı nasıl teselli edeceğini detaylıca anlatıyoruz.
system_prompt = """
Sen Kuran ve Sünnet ışığında şefkatle teselli veren manevi bir rehbersin.
Kullanıcıyı anla, asla yargılama ve derdine uygun 1 ayet ve 1 hadis ile kısa, anlaşılır bir teselli ver. Asla fetva verme.

Cevabın şu yapıda olmalı:
1.  **Halin Anlaşıldı (Şefkatli bir başlangıç):** Kullanıcının duygusunu anladığını belirt.
2.  **Manevi Reçete (Ayet ve Hadis):** İlgili ayet ve hadisi "Kuran'dan bir Işık" ve "Sünnetten bir Müjde" başlıklarıyla ver.
3.  **Huzur Veren Nasihat (Özet):** Kullanıcının kalbini ferahlatacak, dertlerine derman olacak kısa bir nasihat ekle.
4.  **Sünnetten Bir İz (Sünnet Davranışı):** "Peygamber Efendimiz (SAV) böyle durumlarda şöyle yapardı:" başlığı altında, kullanıcının derdiyle ilgili, Peygamberimizin (SAV) uyguladığı somut bir sünnet davranışını (dua etmek, sabretmek, sadaka vermek, abdest almak gibi) yaz.
"""

# 2. Sayfa Konfigürasyonu ve Görsel Öğeler
# Uygulamanın tarayıcı sekmesindeki başlığını ve ikonunu ayarlıyoruz.
st.set_page_config(
    page_title="Manevi Rehber - Huzur Kapısı", 
    page_icon="🌿", 
    layout="centered"
)

# --- GÖRSEL ZENGİNLEŞTİRME ---

# A. Arka Plan ve Genel Tema
# Streamlit'in dahili temalarını kullanabiliriz. "Settings" -> "Theme" kısmından "Light" veya "Dark" seçilebilir.
# Ama daha özelleştirilmiş bir his için CSS kullanabiliriz (Profesyonel olmayanlar için biraz karmaşık olabilir, 
# o yüzden şimdilik Streamlit'in kendi bileşenlerini kullanacağız).

# B. Banner (Üst Görsel)
# Uygulamanın üstüne, huzur veren bir görsel ekleyelim. 
# "ManeviRehber_Banner.jpg" adında bir görseli GitHub deponuza yükleyip, yolunu buraya yazabilirsiniz. 
# Eğer görsel yüklemek istemezseniz, bu satırı silebilirsiniz.
st.image("ManeviRehber_Banner.jpg", use_column_width=True) # GitHub deponuzda bu görsel olmalı.

# C. Başlık ve Alt Başlık
# Markdown kullanarak başlıkları daha şık yapabiliriz.
st.markdown("<h1 style='text-align: center; color: #2E8B57;'>🌿 Manevi Rehber 🌿</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #555;'>Derdini yaz, Kuran, Sünnet ve Nasihat Işığında Teselli Bul...</p>", unsafe_allow_html=True)
st.write("---") # Yatay bir çizgi ekleyelim.

# D. Örnek Butonlar (İsteğe Bağlı)
# Kullanıcıların dertlerini daha kolay seçebilmeleri için hazır butonlar ekleyebiliriz.
# (Bunu sonraki aşamalarda ekleyebiliriz).

# --- UYGULAMA MANTIĞI ---

# Kullanıcının metin gireceği kutu
kullanici_derdi = st.text_area("İçinden geçenleri buraya yazabilirsin:", height=150)

# Gönder butonu
if st.button("Huzur Bul"):
    if kullanici_derdi:
        with st.spinner("Kalbinize inşirah, ruhunuza ferahlık aranıyor..."):
            # Yapay zekaya komutu ve kullanıcının derdini gönderiyoruz
            tam_mesaj = f"{system_prompt}\n\nKullanıcının Derdi: {kullanici_derdi}"
            cevap = model.generate_content(tam_mesaj)
            
            # --- CEVABI GÖRSEL OLARAK DÜZENLEME ---
            
            # Gelen cevabı daha şık bir şekilde gösterelim.
            st.success("İşte Kalbinize Dokunacak Teselli:")
            
            # Markdown ile başlıkları ve metni biçimlendiriyoruz.
            st.markdown(f"""
            ### 🫂 Halin Anlaşıldı
            {cevap.text.split('**')[0]}  # Yapay zekanın cevabındaki ilk bölümü alıyoruz (Şefkatli Başlangıç)
            
            ### 📖 Kuran'dan bir Işık
            {cevap.text.split('**')[1]} # Ayet bölümünü alıyoruz
            
            ### 🕊️ Sünnetten bir Müjde
            {cevap.text.split('**')[2]} # Hadis bölümünü alıyoruz
            
            ### 💡 Huzur Veren Nasihat
            {cevap.text.split('**')[3]} # Nasihat bölümünü alıyoruz
            
            ### ⭐ Sünnetten Bir İz
            {cevap.text.split('**')[4]} # Sünnet davranışı bölümünü alıyoruz
            """)
            
            # --- KODUN SONU ---
    else:
        st.warning("Lütfen önce yukarıdaki kutuya bir şeyler yazın.")
