import sys
import requests
from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont
import time
import config  # config.py'den API bilgilerini alıyoruz

# Pi-hole API'den veri çekme fonksiyonu
def get_pihole_data():
    try:
        params = {
            "auth": config.API_TOKEN,
            "stats": True
        }
        response = requests.get(config.PIHOLE_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API veri çekme hatası: {e}")
        return None

# Ekranda veri gösterme fonksiyonu
def display_pihole_stats():
    # Ekranı başlatma
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear()

    # Yeni bir görüntü oluşturma (beyaz zemin)
    image = Image.new('1', (epd.width, epd.height), 255)  
    draw = ImageDraw.Draw(image)

    # Yazı tipi
    font = ImageFont.load_default()

    # Pi-hole'dan veri al
    data = get_pihole_data()
    if data:
        blocked_queries = data['domains_being_blocked']
        dns_queries_today = data['dns_queries_today']
        ads_blocked_today = data['ads_blocked_today']

        # Yazıları ekrana yazdırma
        draw.text((10, 10), "Pi-hole Stats", font=font, fill=0)
        draw.text((10, 30), f"Blocked Queries: {blocked_queries}", font=font, fill=0)
        draw.text((10, 50), f"DNS Queries Today: {dns_queries_today}", font=font, fill=0)
        draw.text((10, 70), f"Ads Blocked Today: {ads_blocked_today}", font=font, fill=0)
    else:
        draw.text((10, 30), "Unable to fetch data", font=font, fill=0)

    # Ekranda göster
    epd.display(epd.getbuffer(image))
    time.sleep(10)  # 10 saniye sonra ekranı temizler

if __name__ == "__main__":
    display_pihole_stats()
