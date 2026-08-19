import cloudscraper

API_URL = "https://data-reality.com/domain.php"
CHANNEL_ID = "zirve"
BASE_DOMAIN = "https://99baywintv.live/"

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

req_headers = {
    "Referer": BASE_DOMAIN,
    "Origin": BASE_DOMAIN.rstrip('/'),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

def main():
    try:
        # 1. API'den Base URL'i al
        response = scraper.get(API_URL, headers={"User-Agent": req_headers["User-Agent"]}, timeout=15)
        
        if response.status_code == 200:
            base_url = response.json().get("baseurl", "")
            
            if base_url:
                if not base_url.endswith('/'): 
                    base_url += '/'
                raw_m3u8_link = f"{base_url}{CHANNEL_ID}/mono.m3u8"
                
                # 2. KRİTİK ADIM: Asıl video sunucusuna gidip Cloudflare'i çöz ve Cookie topla
                print("Cloudflare aşılıyor ve Cookie'ler toplanıyor...")
                scraper.get(raw_m3u8_link, headers=req_headers, timeout=15)
                
                # Toplanan çerezleri metne çevir
                cookie_str = "; ".join([f"{c.name}={c.value}" for c in scraper.cookies])
                
                # 3. Tüm zorunlu başlıkları (Cookie dahil) Player formatında birleştir
                headers_string = f"User-Agent={req_headers['User-Agent']}&Referer={req_headers['Referer']}&Origin={req_headers['Origin']}&Accept={req_headers['Accept']}"
                
                if cookie_str:
                    headers_string += f"&Cookie={cookie_str}"
                    
                player_format = f"{raw_m3u8_link}|{headers_string}"
                
                with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                    f.write(player_format)
                print("Başarılı! Link ve Cloudflare Cookie'leri dosyaya yazıldı.")
            else:
                with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                    f.write("HATA_BASEURL_YOK|User-Agent=hata")
        else:
            with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
                f.write(f"HATA_HTTP_{response.status_code}|User-Agent=hata")
                
    except Exception as e:
        print("Sistem Hatası:", e)
        with open("ceydus2.m3u8", "w", encoding="utf-8") as f:
            f.write("HATA_SISTEM|User-Agent=hata")

if __name__ == "__main__":
    main()
