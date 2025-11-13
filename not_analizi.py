import streamlit as st
import numpy as np
import pandas as pd
from io import StringIO

#Uygulama Yapılandırması
st.set_page_config(layout="wide") #Sayfayı daha geniş kullanmak için


#Başlık ve Giriş
# st.title fonksiyonu web sayfasının en büyük başğını atar
st.title("Çoklu Ders Not Analiz Uygulaması")
st.markdown("Bu uygulama ile **çoklu ders** notlarınızı analiz edin, **geçme notunu ayarlayın** ve **düzenlenmiş veriyi indirin**.")



#CSV Yükleyici
st.sidebar.header("1. Ver Yükleme")
yuklenen_dosya = st.sidebar.file_uploader(
    "Lütfen Not Verisi İçeren Excel veya CSV Dosyasını Yükleyin",
    type=["csv", "xlsx", "xls"]
)

#Eğer dosya yüklenmişse ana analiza başla
if yuklenen_dosya is not None:

    @st.cache_data
    def load_data(file):
        #Dosya uzantısını kontrol edelim
        if file.name.endswith('.csv'):
            return pd.read_csv(file, sep=';')
        elif file.name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file, engine='openpyxl') #Excel dosyasını openpyxl kütüphanesi ile okur
        else:
            st.error("Desteklenmeyen dosya formatı !") 
            st.stop()
    try:
        df = load_data(yuklenen_dosya)
        #Sadece sayısal sütunları seç(Çoklu Ders analizi için hazırlık)
        sayisal_df = df.select_dtypes(include=np.number)

        #Eğer veri yüklenmiş ancak sayısal sütun yoksa uyarı verir
        if sayisal_df.empty:
            st.error("Yüklediğiniz dosyada analiz edilebilecek sayısal not sütunu bulunamadı")
            st.stop()
        
        #DataFrame'i NumPy matrisine çevir(Hızlı olması için)
        not_matrisi = sayisal_df.values

        #Sütun isimlerini al(Ders adları)
        ders_adlari = sayisal_df.columns.tolist()
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        st.stop()

#İnteraktif Ayarlar ve Analiz 
    st.sidebar.header("2. Analiz Ayarları")

    #Geçme notu slider'ı
    gecme_notu = st.slider(
        "Geçme Notu (Tüm Dersler İçin):",
        min_value=0, max_value=100, value=50
    )

    #Çan Eğrisi Puanı
    ek_puan = st.sidebar.number_input(
        "Tüm Notlara Eklenecek Bonus Puan (Çan Eğrisi):",
        min_value=0, max_value=10, value=0
    )
    
    st.header("1. Ders Bazlı Genel Analiz")
    #Tüm Derslerin Ortalaması, En Büyük ve En Düşük Notlar
    ortalama_notlar = np.mean(not_matrisi, axis=0)
    en_yuksek_notlar = np.max(not_matrisi, axis=0)
    en_dusuk_notlar = np.min(not_matrisi, axis=0)

    #Metrikleri Gösterme
    cols = st.columns(len(ders_adlari))
    for i, ders in enumerate(ders_adlari):
        with cols[i]:
            st.subheader(f"___{ders}___")
            st.metric(label="Ortalama", value=f"{ortalama_notlar[i]:.2f}")
            st.metric(label="Maksimum Not", value=int(en_yuksek_notlar[i]))
            st.metric(label="Minimum Not", value=int(en_dusuk_notlar[i]))

    st.markdown("---")

    #Geçme Kalma Analizi
    st.header("2. Geçme/Kalma ve Başarı Oranı")

    gecme_makesi = not_matrisi >= gecme_notu #Geçenlerin maskesi
    gecen_sayilari = np.sum(gecme_makesi, axis=0)
    toplam_ogrenci = not_matrisi.shape[0]

    cols_g = st.columns(len(ders_adlari))
    for i, ders in enumerate(ders_adlari):
        with cols_g[i]:
            st.metric(
                label=f"{ders} Başarı Oranı",
                value=f"% {((gecen_sayilari[i] / toplam_ogrenci) * 100):.1f}",
                delta=f"{gecen_sayilari[i]} Kişi Geçti"
            )
    st.markdown("---")

    #Notlara Ekleme ve Kırpma (Çan eğrisi)
    st.header("3. Düzenlenmiş Notlar ve İndirme")

    if ek_puan > 0:
        #Tüm matrisi tek seferde topla ve 0-100 aralığında kırp
        duzenlenmis_notlar = np.clip(not_matrisi + ek_puan, 0 , 100)

        #Yeni ortalamayı hesapla ve göster
        yeni_ortalama = np.mean(duzenlenmis_notlar, axis=0)

        yeni_df = pd.DataFrame(duzenlenmis_notlar, columns=[f"{d}_YENİ" for d in ders_adlari])

        st.success(f"Tüm notlara başarıyla  {ek_puan} puan eklenmiştir.")

        #Yeni ortalamaları bir tablo olarak gösterelim
        yeni_ort_df = pd.DataFrame({
            'Ders': ders_adlari,
            'Eski Ortalama': [f"{o:.2f}" for o in ortalama_notlar],
            'Yeni Ortalama': [f"{o:.2f}" for o in yeni_ortalama]
        })
        st.dataframe(yeni_ort_df, hide_index=True)

        #Düzenlemiş DataFrame'i oluşturur
        son_df = pd.concat([df.drop(columns=sayisal_df.columns, errors='ignore'),sayisal_df,yeni_df],axis=1)

        #Veriyi indirme
        csv_buffer = StringIO()
        son_df.to_csv(csv_buffer,index=False)
        csv_verisi = csv_buffer.getvalue()
        
        st.download_button(
            label="Düzenlenmiş Notları İndir (Yen, CSV)",
            data=csv_verisi,
            file_name='duzenlenmis_notlar.csv',
            mime='text/csv',
            type="primary"
        )
        st.caption("Bu dosyada orjinal notlar ve ek puan uygulanmış yeni notlar birlikte bulunmaktadır")
    else:
        #Eğer dosya yüklenmemişse
        st.info("Lütfen sol menüdeki 'Veri Yükleme' alanından bir Excel(.xlsx) veya CSV dosyasını yükleyiniz")

        #Kılavuz için örnek CSV şablonu
        st.subheader("Örnek Veri Yapısı")
        st.caption("Verinizde en az iki sayısal sütun (ders) bulunmalıdır.")
        ornek_veri = {
            'Ogrenci_ID': [101,102,103,104,105],
            'Matematik': [85,45,92,60,78],
            'Fizik': [75,55,70,30,88],
            'Kimya': [65,75,80,50,70]
        }
        ornek_df = pd.DataFrame(ornek_veri)
        st.dataframe(ornek_df,hide_index=True)