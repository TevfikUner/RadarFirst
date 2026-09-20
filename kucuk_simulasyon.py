import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("1. Copernicus hava durumu küpü yükleniyor...")
veri_kupu = xr.open_dataset("ocak_2019_turbulans.nc")

# 2. Simüle edilmiş bir uçuş rotası yaratalım (Ankara -> İstanbul güzergahı)
zamanlar = pd.date_range(start="2019-01-01 12:00:00", periods=10, freq="10min")
enlemler = np.linspace(39.9, 41.0, 10)  # Ankara'dan İstanbul'a enlem değişimi
boylamlar = np.linspace(32.8, 29.0, 10) # Ankara'dan İstanbul'a boylam değişimi

ucus_rotasi = pd.DataFrame({
    'zaman': zamanlar,
    'enlem': enlemler,
    'boylam': boylamlar,
    'irtifa_hpa': 250.0 # Seyir irtifası
})

print("\n2. Uçuş rotası ile hava durumu verisi eşleştiriliyor...")
turbulans_sonuclari = []

for index, satir in ucus_rotasi.iterrows():
    # O anki koordinata en yakın hava durumu verisini Copernicus küpünden çekiyoruz
    nokta_hava = veri_kupu.sel(
        valid_time=satir['zaman'],
        pressure_level=satir['irtifa_hpa'],
        latitude=satir['enlem'],
        longitude=satir['boylam'],
        method="nearest"
    )
    
    u = float(nokta_hava['u'].values)
    v = float(nokta_hava['v'].values)
    w = float(nokta_hava['w'].values)
    
    # Basitleştirilmiş EDR (Türbülans Şiddeti) tahmini
    ruzgar_siddeti = np.sqrt(u**2 + v**2)
    edr = np.cbrt(np.abs(w * ruzgar_siddeti)) * 0.1
    turbulans_sonuclari.append(edr)

ucus_rotasi['hesaplanan_edr'] = turbulans_sonuclari

print("\n3. Simülasyon Sonuç Tablosu:")
print(ucus_rotasi[['zaman', 'enlem', 'boylam', 'hesaplanan_edr']])

# 4. Görselleştirme: Rota üzerindeki türbülans haritası
plt.figure(figsize=(9, 5))
# cursor_y hatası düzeltildi
plt.plot(ucus_rotasi['boylam'], ucus_rotasi['enlem'], marker='o', color='blue', label='Uçuş Rotası')
plt.scatter(ucus_rotasi['boylam'], ucus_rotasi['enlem'], c=ucus_rotasi['hesaplanan_edr'], cmap='Reds', s=100, edgecolor='black', label='Türbülans Şiddeti (EDR)')
plt.colorbar(label='EDR Şiddeti')

plt.title("Test: Rota Uzerindeki Turbulans (Gecici Gorsel)")
plt.xlabel("Boylam")
plt.ylabel("Enlem")
plt.grid(True)
plt.legend()
plt.show()


