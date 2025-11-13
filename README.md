📊 İnteraktif Çoklu Ders Not Analiz Uygulaması :

Bu proje, Python'ın NumPy ve Pandas kütüphanelerinin gücünü, Streamlit kullanılarak oluşturulmuş interaktif bir web arayüzü ile birleştirir. Uygulama, kullanıcının yüklediği Excel veya CSV dosyalarındaki not verilerini anlık olarak analiz eder, ders bazlı istatistikler sunar ve uygulanan bonus puanlarla (Çan Eğrisi) birlikte yeni bir veri seti indirme imkanı sağlar.

✨ Temel Özellikler
Veri Esnekliği: Hem Excel (.xlsx, .xls) hem de CSV dosyalarını yükleme desteği.

Çoklu Ders Analizi: Yüklenen dosyadaki tüm sayısal sütunları (ders notlarını) otomatik olarak tanıma ve ayrı ayrı analiz etme.

İnteraktif Ayarlar: Geçme notunu ve tüm notlara eklenecek bonus puanı (np.clip ile 0-100 arasında sınırlandırılmış) anlık olarak ayarlayabilme.

NumPy Hızı: Tüm istatistiksel hesaplamaların (ortalama, başarı oranı, en yüksek/düşük not) büyük veri setleri üzerinde bile NumPy'nin vektörel işlemleri sayesinde çok hızlı yapılması.

Veri Çıktısı: Düzenlenmiş notları (bonus puan eklenmiş yeni sütunlar dahil) yeni bir CSV dosyası olarak indirme (st.download_button).

🛠️ Kullanılan Teknolojiler
Python 3.x

NumPy: Yüksek performanslı sayısal hesaplamalar ve matris işlemleri için.

Pandas: Excel ve CSV verilerini okuma, temizleme ve DataFrame yönetimi için.

Streamlit: Veri analiz scriptini interaktif web uygulamasına dönüştürmek için.

openpyxl: Excel (.xlsx) dosyalarını okumak için gerekli yardımcı kütüphane.

<img width="1920" height="1080" alt="Ekran görüntüsü 2025-11-13 154349" src="https://github.com/user-attachments/assets/7b66f0af-1702-4200-8753-a961f1bc6249" />
<img width="1920" height="1080" alt="Ekran görüntüsü 2025-11-13 154410" src="https://github.com/user-attachments/assets/aed7a7f1-6793-4601-87eb-d8b0e082cfef" />
