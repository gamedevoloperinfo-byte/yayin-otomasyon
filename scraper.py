import cloudscraper
import json

# Hedeflerimiz değişti: Artık iframe HTML'ine değil, doğrudan veriyi veren API'ye gidiyoruz.
API_URL = "https://data-reality.com/domain.php"
CHANNEL_ID = "zirve"
BASE_DOMAIN = "https://99baywintv.live/"

# Cloudflare engeli ihtimaline karşı scraper kullanmaya devam ediyoruz
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

req_headers = {
    "Referer": BASE_DOMAIN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def main():
    try:
        # 1. API'ye gidip güncel sunucu adresini (Base URL) alıyoruz
        response = scraper.get(API_URL, headers=req_headers, timeout=15)
        print(f"API Durum Kodu: {response.status_code}")
        
        if response.status_code == 200:
            # 2. Gelen veriyi JSON olarak oku
            data = response.json()
            base_url = data.get("baseurl", "")
            
            if base_url:
                print(f"Güncel Sunucu Bulundu: {base_url}")
                
                # Linkin sonunda slash (/) yoksa ekle
                if not base_url.endswith('/'):
                    base_url += '/'
                    
                # 3. JavaScript'in yaptığı gibi linki biz birleştiriyoruz
                raw_m3u8_link = f"{base_url}{CHANNEL_ID}/mono.m3u8"
                print(f"Oluşturulan Yayın Linki: {raw_m3u8_link}")
                
                # 4. Senin ExoPlayer'ın anlayacağı Link|Header formatını oluştur
                player_format = f"{raw_m3u8_link}|Referer={BASE_DOMAIN}&Origin={BASE_DOMAIN.rstrip('/')}&User-Agent={req_headers['User-Agent']}"
                
                # 5. Dosyaya kaydet
                with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                    f.write(player_format)
                print("Tebrikler! Link başarıyla ceydus2.m3u8 dosyasına yazıldı.")
                
            else:
                print("Hata: JSON içinde 'baseurl' bulunamadı.")
                with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                    f.write("HATA_BASEURL_YOK|Referer=hata")
        else:
            print("API'ye erişilemedi.")
            with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                f.write(f"HATA_HTTP_{response.status_code}|Referer=hata")
                
    except Exception as e:
        print("Sistem Hatası:", e)
        with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
            f.write("HATA_SISTEM|Referer=hata")

if __name__ == "__main__":
    main()
