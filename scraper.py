import cloudscraper
import re

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
        if response.status_code == 200:
            html = response.text
            match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\']*)', html)
            
            if match:
                raw_m3u8_link = match.group(1)
                # Player'ın için Link|Header formatını oluştur
                player_format = f"{raw_m3u8_link}|Referer={BASE_DOMAIN}&Origin={BASE_DOMAIN.rstrip('/')}&User-Agent={req_headers['User-Agent']}"
                
                # Dosyaya yaz
                with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                    f.write(player_format)
                print("Başarılı!")
    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    main()
