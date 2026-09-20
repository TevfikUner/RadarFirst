import xarray as xr
import pandas as pd
import numpy as np
import folium

print("1. Veriler hazırlanıyor...")
veri_kupu = xr.open_dataset("ocak_2019_turbulans.nc")

# Ankara -> İstanbul uçuş simülasyonu
zamanlar = pd.date_range(start="2019-01-01 12:00:00", periods=10, freq="10min")
enlemler = np.linspace(39.9, 41.0, 10)
boylamlar = np.linspace(32.8, 29.0, 10)

ucus_rotasi = pd.DataFrame({
    'zaman': zamanlar,
    'enlem': enlemler,
    'boylam': boylamlar,
    'irtifa_hpa': 250.0
})

turbulans_sonuclari = []
for indeks, satir in ucus_rotasi.iterrows():
    nokta = veri_kupu.sel(
        valid_time=satir['zaman'],
        pressure_level=satir['irtifa_hpa'],
        latitude=satir['enlem'],
        longitude=satir['boylam'],
        method="nearest"
    )
    
    u = float(nokta['u'].values)
    v = float(nokta['v'].values)
    w = float(nokta['w'].values)
    
    ruzgar_siddeti = np.sqrt(u**2 + v**2)
    edr = np.cbrt(np.abs(w * ruzgar_siddeti)) * 0.1
    turbulans_sonuclari.append(edr)

ucus_rotasi['hesaplanan_edr'] = turbulans_sonuclari

print("2. İnteraktif harita oluşturuluyor...")
# Haritayı rotanın tam merkezine odaklayarak başlatıyoruz. Havacılık teması için koyu renkli harita seçtik.
merkez_enlem = ucus_rotasi['enlem'].mean()
merkez_boylam = ucus_rotasi['boylam'].mean()
ucus_haritasi = folium.Map(location=[merkez_enlem, merkez_boylam], zoom_start=7, tiles="CartoDB dark_matter")

# Rotayı sürekli bir çizgi olarak ekleyelim
koordinatlar = list(zip(ucus_rotasi['enlem'], ucus_rotasi['boylam']))
folium.PolyLine(koordinatlar, color="#3388ff", weight=3, opacity=0.8).add_to(ucus_haritasi)

# Her bir noktayı EDR şiddetine göre renklendirerek haritaya ekleyelim
for indeks, satir in ucus_rotasi.iterrows():
    edr_degeri = satir['hesaplanan_edr']
    
    # Türbülans şiddetine göre dinamik renk ataması
    if edr_degeri < 0.06:
        renk = "green"  # Sakin
    elif edr_degeri < 0.08:
        renk = "orange" # Hafif sarsıntı
    else:
        renk = "red"    # Türbülans riski
        
    # Tıklandığında açılacak bilgi penceresi
    aciklama = f"<b>Saat:</b> {satir['zaman'].strftime('%H:%M')}<br><b>İrtifa:</b> 250 hPa<br><b>EDR:</b> {edr_degeri:.4f}"
    
    folium.CircleMarker(
        location=[satir['enlem'], satir['boylam']],
        radius=7,
        popup=folium.Popup(aciklama, max_width=250),
        color=renk,
        fill=True,
        fill_color=renk,
        fill_opacity=0.9
    ).add_to(ucus_haritasi)

# Haritayı HTML dosyası olarak kaydet
dosya_adi = "turbulans_haritasi.html"
ucus_haritasi.save(dosya_adi)
print(f"3. İşlem tamam! Sol taraftaki dosya listesinden '{dosya_adi}' dosyasına sağ tıklayıp tarayıcıda açabilirsin.")