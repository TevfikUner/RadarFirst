import pandas as pd
import xarray as xr

print("Hava durumu veri küpü yükleniyor...")
veri_kupu = xr.open_dataset("ocak_2019_turbulans.nc")
df_hava = veri_kupu.to_dataframe().reset_index()

# Not: OpenSky veritabanı erişimin tam olarak senkronize olup açıldığında, 
# çekeceğimiz uçuş verisi DataFrame formatında buraya gelecektir.
# Örnek bir uçuş verisi simülasyonu (Test amaçlı):
ornek_ucus_verisi = pd.DataFrame({
    'zaman': pd.to_datetime(['2019-01-01 12:00:00']),
    'enlem': [39.9],
    'boylam': [32.8],
    'irtifa_hpa': [250.0],
    'dikey_hiz': [-1.5] # EDR hesabı için uçağın dikey hareketi
})

print("\nÖrnek Uçuş Verisi:")
print(ornek_ucus_verisi)

# Burada iki tabloyu zaman, enlem, boylam ve basınç seviyesi üzerinden 
# en yakın koordinat mantığıyla birbirine bağlayacağız (Merge/Join işlemi).
print("\n[Bilgi]: OpenSky bağlantı izni tam olarak aktifleştiğinde, bu iskelet kod üzerine")
print("gerçek uçuş rotalarını ekleyip hava durumuyla saniy軸 bazında eşleştireceğiz.")