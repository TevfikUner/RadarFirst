import numpy as np
import pandas as pd

def edr_hesapla(dikey_hiz_degisimi, hava_yogunlugu=1.225):
    """
    Uçağın dikey hızındaki ani sapmaları ve atmosferik parametreleri 
    kullanarak basitleştirilmiş EDR (Türbülans Şiddeti) tahmini yapar.
    """
    # Havacılık standartlarında EDR hesaplama yaklaşımı (Matematiksel İskelet)
    # dikey_hiz_degisimi (vertrate): m/s cinsinden dikey ivmelenme/sapma
    
    # Mutlak dikey hız değişiminin küpkökü tabanlı EDR türetmesi
    edr_degeri = np.cbrt(np.abs(dikey_hiz_degisimi)) * 0.15
    
    return round(edr_degeri, 4)

# --- Test Edelim ---
# Örnek bir uçuş satırı simüle edelim: Uçağın dikey hızında ani bir 2.5 m/s'lik sapma olsun
ornek_vertrate = 2.5
hesaplanan_edr = edr_hesapla(ornek_vertrate)

print(f"Uçağın dikey hız değişimi: {ornek_vertrate} m/s")
print(f"Hesaplanan Türbülans Şiddeti (EDR): {hesaplanan_edr}")