import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# İlk URL'den tabloyu çekme
url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?endeks=03#page-1"
r = requests.get(url)
s = BeautifulSoup(r.text, "html.parser")

# Tabloyu çek ve işle
tablo = s.find("table", {"id": "summaryBasicData"})
tablo = pd.read_html(str(tablo), flavor="bs4")[0]  # [0] ile ilk tabloyu alıyoruz

# Tablo sütunlarını kontrol et
print("Sütunlar:", tablo.columns)

# "Kod" sütunundan hisse isimlerini çekme
hisseler = tablo["Kod"].tolist()  # "Kod" sütunundaki tüm hisseleri listeye çeviriyoruz

# Tüm hisseler için veri çekme ve hesaplama
tum_sonuclar = []

for hisse in hisseler:
    parametreler = (
        ("hisse", hisse),
        ("startdate", "28-11-2023"),
        ("enddate", "28-10-2024"),
    )
    
    url2 = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?"
    r2 = requests.get(url2, params=parametreler).json().get("value", [])
    
    if r2:  # Eğer veri varsa
        # Veriyi DataFrame'e çevirme
        veri = pd.DataFrame.from_dict(r2)
        veri = veri.iloc[:, 0:3]  # İlk üç sütunu alıyoruz
        veri = veri.rename({"HGDG_HS_KODU": "Hisse", "HGDG_TARIH": "Tarih", "HGDG_KAPANIS": "Fiyat"}, axis=1)
        
        # Tarih ve fiyat verilerini düzenliyoruz
        veri = veri[["Tarih", "Fiyat"]]
        veri["Fiyat"] = pd.to_numeric(veri["Fiyat"], errors="coerce")  # Fiyatları sayıya çevir
        
        # Getiri ve oynaklık hesaplama
        if not veri["Fiyat"].isnull().all():  # Fiyat sütunu boş değilse
            gelir = veri["Fiyat"].pct_change().mean() * 252  # Yıllık getiri
            oynaklik = veri["Fiyat"].pct_change().std() * np.sqrt(252)  # Yıllık oynaklık
            tum_sonuclar.append({"Hisse": hisse, "Gelir": gelir, "Oynaklık": oynaklik})

# Sonuçları bir DataFrame'e çevir
sonuc_df = pd.DataFrame(tum_sonuclar)

# Sonuçları yazdır
print(sonuc_df)

# Sonuçları CSV olarak kaydetme
dosya_yolu = r"C:/Users/hp/OneDrive/Masaüstü/bist30_sonuclar.csv"  # Dosya yolu ve adı
sonuc_df.to_csv(dosya_yolu, index=False, encoding="utf-8-sig")  # CSV olarak kaydet

print(f"Sonuçlar başarıyla {dosya_yolu} konumuna kaydedildi.")
