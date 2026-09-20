import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# 1. Hava durumu veri küpünü belleğe yükle
veri_kupu = xr.open_dataset("ocak_2019_turbulans.nc")

# 2. Belirli bir anı ve irtifayı filtrele (Örn: 1 Ocak 2019 saat 12:00, 250 hPa irtifa)
zaman = "2019-01-01T12:00:00"
irtifa = 250.0

# 3. O ana ait U ve V rüzgar bileşenlerini çek
u_ruzgar = veri_kupu['u'].sel(valid_time=zaman, pressure_level=irtifa)
v_ruzgar = veri_kupu['v'].sel(valid_time=zaman, pressure_level=irtifa)

# 4. Rüzgarın toplam şiddetini hesapla (kök(u^2 + v^2))
ruzgar_siddeti = np.sqrt(u_ruzgar**2 + v_ruzgar**2)

# 5. Görselleştirme (Matplotlib ile harita çizimi)
plt.figure(figsize=(10, 6))

# Rüzgar şiddetini bir ısı haritası (jet renk paleti) olarak çiz
ruzgar_siddeti.plot(cmap='jet', cbar_kwargs={'label': 'Rüzgar Şiddeti (m/s)'})

plt.title(f"Türkiye Üzeri Jet Akımları ve Rüzgar Şiddeti\nTarih: 1 Ocak 2019 12:00 | İrtifa: {irtifa} hPa")
plt.xlabel("Boylam")
plt.ylabel("Enlem")

# Haritayı ekranda göster
plt.show()