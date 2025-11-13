import streamlit as st
import numpy as np


#Başlık ve Giriş
# st.title fonksiyonu web sayfasının en büyük başğını atar
st.title("Not Analizi Uygulaması")
st.write("Bu uygulama, öğrenci notlarını analiz etmek için kullanılır. Notları girin ve çeşitli istatistikleri hesaplayın.")


#Veri Setini oluşturma 
# @st.cache_data dekaratörü, fonksiyonun çıktısını hafuzada tutar .Böylece slider her oynadığında
# veriyi baştan hesaplamakla uğraşmaz, hız kazandırır.

@st.cache_data
def create_datase():
    #Her seferinde aynı "rastgele" veriyi almak için
    np.random.seed(42)
    #0 - 100 arasında 1000 tane not
    notlar = np.random.randint(0, 101, size=1000)
    return notlar

notlar = create_datase()


#Sınıf İstatisliklerini Gösterme
#st.header() alt başlıkları oluşturur
st.header("Genel Sınıf İstatistikleri")

#st.metric() bir kutu içinde istatistik göstermek için kullanırız.
#st.columns() sayfayı sütunlara ayırmamızı sağlar
ortalama = np.mean(notlar) # np.mean()fonksiyonu bir veri kümesinin aritmetik ortalamasını(average) hesaplar
en_yuksek = np.max(notlar)
en_dusuk = np.min(notlar)

col1, col2, col3 = st.columns(3) #Colon isimlerine göre colon ürettik
col1.metric(label="Sınıf Ortalaması", value=f"{ortalama:.2f}") # Ortalamadan gelen sayı değerinin ondalık kısmını 2 hane ile sınırladık
col2.metric(label="En Yüksek Not", value=en_yuksek)
col3.metric(label="En Düşük Not", value=en_dusuk)


# İNTERAKTİF BÖLÜM
st.header("İnteraktif Geçme/Kalma Analizi")

#st.slider() kullanıcıya bir kaydırgaç sunar
#0-100 arası, varsayılan değeri 50 olan bir slider:
gecme_notu = st.slider("Geçme Notunu Seçiniz:", min_value=0, max_value=100, value=50)

#Kullanıcının seçimine göre yeniden hesaplama
gecen_sayisi = np.sum(notlar >= gecme_notu)
kalan_sayisi = np.sum(notlar < gecme_notu)
gecme_orani = (gecen_sayisi / 1000) * 100

st.write(f"Seçtiğiniz geçme notu: **{gecme_notu}")

col1,col2 = st.columns(2)
col1.metric(label="Geçen Öğrenci Sayısı", value=gecen_sayisi)
col2.metric(label="Kalan Öğrenci Sayısı", value=kalan_sayisi)

st.metric(label="Sınıf Başarı Oranı", value=f"% {gecme_orani}")

#Veriyi ve Grafiği gösterme
st.header("Ham Veriler ve Dağılım")

#Checkbox ekliyoruz
if st.checkbox("İlk 50 notunu göster"):
    st.write(notlar[:50])

#Streamlit, Numpt verilerini doğrudan grafiğe dökebilir
st.subheader("Not Dağılım Grafiği (Histogram)")

#st.bar_chart() fonksiyonu bir çubuk grafik çizer
#np.histogram() ile hangi nottan kaç adet olduğunu buluruz

hist_degerleri, araliklar = np.histogram(
    notlar, bins=20, range=(0,100) #0-100 arasını 20 çubuğa böl
)

st.bar_chart(hist_degerleri)