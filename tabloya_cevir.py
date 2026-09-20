import xarray as xr
import pandas as pd

print("Hava durumu veri küpü yükleniyor...")
# 1. 4 boyutlu NetCDF küpünü açıyoruz
veri_kupu = xr.open_dataset("ocak_2019_turbulans.nc")

print("Tabloya dönüştürme işlemi başlıyor (Bu birkaç saniye sürebilir)...")
# 2. Xarray küpünü Pandas DataFrame tablosuna çeviriyoruz
# reset_index() ile enlem, boylam, zaman ve basınç sütunlarını normal sütun haline getiriyoruz
df = veri_kupu.to_dataframe().reset_index()

# 3. Tablonun ilk 5 satırını ekrana yazdırarak yapısını kontrol edelim
print("\nOluşan Tablonun İlk 5 Satırı:")
print(df.head())

print(f"\nToplam satır sayısı: {len(df)}")