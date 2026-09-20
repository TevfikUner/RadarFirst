import trino
import pandas as pd

# OpenSky sunucusuna bağlantı oluşturuyoruz
baglanti = trino.dbapi.connect(
    host='trino.opensky-network.org',
    port=443,
    user='tevfik0',
    http_scheme='https',
    auth=trino.auth.BasicAuthentication("tevfik0", "Tevfik_uner1687")
)

imlec = baglanti.cursor()

# Ban yememek için alanı (Türkiye) ve zamanı (1 Ocak 2019, 00:00 - 01:00 UTC) çok dar tuttuğumuz test sorgusu
sorgu = """
SELECT time, icao24, lat, lon, velocity, heading, vertrate, geoaltitude
FROM state_vectors_data4
WHERE time >= 1546300800 AND time <= 1546304400
AND lat >= 36 AND lat <= 42
AND lon >= 26 AND lon <= 45
LIMIT 10
"""

imlec.execute(sorgu)
sonuclar = imlec.fetchall()

# Gelen veriyi işleyebilmek için bir tabloya (DataFrame) aktarıyoruz
sutunlar = ['zaman', 'ucak_id', 'enlem', 'boylam', 'hiz', 'yon', 'dikey_hiz', 'irtifa']
ucuslar = pd.DataFrame(sonuclar, columns=sutunlar)

print(ucuslar)