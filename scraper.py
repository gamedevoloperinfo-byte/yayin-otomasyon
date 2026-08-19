import cloudscraper
import re
import os

TARGET_URL = "https://99baywintv.live/channel?id=zirve"
BASE_DOMAIN = "https://99baywintv.live/"

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

req_headers = {
    "Referer": BASE_DOMAIN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def main():
    try:
        response = scraper.get(TARGET_URL, headers=req_headers, timeout=15)
        print(f"HTTP Durum Kodu: {response.status_code}")
        
        if response.status_code == 200:
            html = response.text
            
            # Sayfanın ilk 500 karakterini yazdır (Cloudflare mi yoksa gerçek site mi görelim)
            print("Gelen HTML (İlk 500 karakter):")
            print(html[:500])
            
            match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\']*)', html)
            
            if match:
                raw_m3u8_link = match.group(1)
                player_format = f"{raw_m3u8_link}|Referer={BASE_DOMAIN}&Origin={BASE_DOMAIN.rstrip('/')}&User-Agent={req_headers['User-Agent']}"
                
                with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                    f.write(player_format)
                print("Başarılı! Link bulundu ve dosyaya yazıldı.")
            else:
                print("Hata: Sayfa başarıyla çekildi ama içinde m3u8 linki bulunamadı!")
                # Çökmemesi için boş/hata dosyası oluştur
                with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                    f.write("HATA_LINK_BULUNAMADI|Referer=hata")
        else:
            print("Siteye erişilemedi.")
            with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                f.write("HATA_HTTP_" + str(response.status_code) + "|Referer=hata")
                
    except Exception as e:
        print("Sistem Hatası:", e)
        with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
            f.write("HATA_SISTEM|Referer=hata")

if __name__ == "__main__":
    main()
